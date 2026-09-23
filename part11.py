#!/usr/bin/env python3
"""
part11.py — optional 21 CFR Part 11 hook into a part11-audit-trail service.

A completed 21 CFR 820 SOP review is an electronic record. When PART11_AUDIT_URL is set,
``record_review`` stores the review as a record (PUT /records/sop_review/{id}, which the
service hashes and logs) and appends a ``sop_review:completed`` audit entry
(POST /events) carrying that record hash. A human approver then runs ``sign`` to apply a
Part 11 e-signature (POST /sign, meaning="approved") over the record's hash; it is checked
with the service's own GET /verify-signature/{id}.

When PART11_AUDIT_URL is unset, nothing here runs and sop_review.py behaves as before.

Environment (os.getenv only, never hardcoded):
    PART11_AUDIT_URL    base URL of part11-audit-trail, e.g. http://localhost:8011
    PART11_AUDIT_TOKEN  X-Audit-Token for POST /events (only if the service sets
                        AUDIT_INTERNAL_TOKEN)

Approver usage:
    python part11.py sign --record-id <id> --signer alice     # password prompted
    python part11.py verify --signature-id <id>
"""

import argparse
import getpass
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

RECORD_TYPE = "sop_review"


def base_url() -> str | None:
    url = os.getenv("PART11_AUDIT_URL")
    return url.rstrip("/") if url else None


def _request(method: str, path: str, body: dict | None = None, headers: dict | None = None) -> dict:
    url = base_url()
    if not url:
        raise RuntimeError("PART11_AUDIT_URL is not set")
    req = urllib.request.Request(
        url + path,
        data=None if body is None else json.dumps(body).encode("utf-8"),
        headers={"content-type": "application/json", **(headers or {})},
        method=method,
    )
    with urllib.request.urlopen(req, timeout=10) as resp:  # noqa: S310 (URL is operator config)
        return json.loads(resp.read())


def record_review(review: dict, sop_filename: str, sop_type: str, device_class: str,
                  actor: str | None = None) -> dict:
    """Store a completed review as a Part 11 electronic record and log its audit entry.

    Returns ``{"record_id", "record_hash", "event"}``. The record hash is computed by the
    service (sha256 of canonical JSON), so there is one hashing implementation.
    """
    actor = actor or getpass.getuser()
    now = datetime.now(timezone.utc)
    record_id = f"{Path(sop_filename).stem}-{now:%Y%m%dT%H%M%S%fZ}"
    content = {"sop_filename": sop_filename, "sop_type": sop_type,
               "device_class": device_class, "reviewed_at": now.isoformat(), "review": review}
    state = _request("PUT", f"/records/{RECORD_TYPE}/{record_id}",
                     {"actor": actor, "content": content})
    token = os.getenv("PART11_AUDIT_TOKEN")
    event = _request(
        "POST", "/events",
        {"actor": actor, "action": "sop_review:completed", "record_type": RECORD_TYPE,
         "record_id": record_id, "after_hash": state["current_hash"]},
        {"X-Audit-Token": token} if token else None,
    )
    return {"record_id": record_id, "record_hash": state["current_hash"], "event": event}


def sign_approval(record_id: str, signer: str, password: str) -> dict:
    """Apply the approver's Part 11 e-signature (meaning="approved") over the record hash."""
    return _request("POST", "/sign", {"username": signer, "password": password,
                                      "record_id": record_id, "meaning": "approved"})


def verify_signature(signature_id: str) -> dict:
    return _request("GET", f"/verify-signature/{signature_id}")


def main() -> None:
    ap = argparse.ArgumentParser(prog="part11.py", description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("sign", help="approve a review record (POST /sign, meaning=approved)")
    s.add_argument("--record-id", required=True)
    s.add_argument("--signer", required=True)
    v = sub.add_parser("verify", help="GET /verify-signature/{id}")
    v.add_argument("--signature-id", required=True)
    args = ap.parse_args()

    if not base_url():
        sys.exit("ERROR: PART11_AUDIT_URL is not set.")
    try:
        if args.cmd == "sign":
            # Password is prompted, never taken from argv or env, so it is not logged.
            result = sign_approval(args.record_id, args.signer,
                                   getpass.getpass(f"Password for {args.signer}: "))
        else:
            result = verify_signature(args.signature_id)
    except urllib.error.HTTPError as exc:
        sys.exit(f"ERROR: part11-audit-trail returned {exc.code}: {exc.read().decode()}")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
