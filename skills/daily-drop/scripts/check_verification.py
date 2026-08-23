#!/usr/bin/env python3
"""
Daily Drop verification gate — Stage 4 of the daily publishing run.

Checks a verification manifest (written after WebFetch/CurAItion source
checks) against the story package it verifies. This script checks the
BOOKKEEPING; the actual fetching is done with the WebFetch tool and CurAItion
MCP calls, never by this script.

HARD failures (exit 1):
  - a fact in the package's facts[] with no entry in the manifest
  - a fact entry with no verdict, or a citation with no status
  - a fact whose verdict is "failed" (all citations dead/mismatched) —
    failed facts must be removed from the working set and the package
    re-validated before writing starts
  - a fact marked "verified" with no citation whose status is "verified"
  - an "unreachable" fact with no verified citation (treat as failed)

Prints the verified-URL allowlist on success (one URL per line, prefixed
"ALLOW ") so the caller can hand it to cross_check.py.

Usage:
    python check_verification.py verification-<date>.json \
        --package story-package-<date>.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

FACT_VERDICTS = {"verified", "failed", "unreachable"}
CITE_STATUSES = {"verified", "mismatch", "dead", "unreachable"}


def main() -> int:
    ap = argparse.ArgumentParser(description="Daily Drop verification gate.")
    ap.add_argument("manifest", type=Path)
    ap.add_argument("--package", type=Path, required=True)
    args = ap.parse_args()

    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    pkg = json.loads(args.package.read_text(encoding="utf-8"))

    fails = []
    entries = {f.get("fact_id"): f for f in manifest.get("facts", [])}

    pkg_fact_ids = [f.get("id") or f.get("fact_id")
                    for f in pkg.get("facts", [])]
    for fid in pkg_fact_ids:
        if fid not in entries:
            fails.append("fact %r has no verification entry" % fid)

    allow = set()
    counts = {"verified": 0, "failed": 0, "unreachable": 0}
    for fid, e in entries.items():
        verdict = e.get("verdict")
        if verdict not in FACT_VERDICTS:
            fails.append("fact %r: missing/unknown verdict %r" % (fid, verdict))
            continue
        counts[verdict] += 1
        cites = e.get("citations", [])
        if not cites:
            fails.append("fact %r: no citations recorded" % fid)
        n_verified = 0
        for c in cites:
            status = c.get("status")
            if status not in CITE_STATUSES:
                fails.append("fact %r: citation %r has missing/unknown "
                             "status %r" % (fid, c.get("url"), status))
            elif status == "verified":
                n_verified += 1
                if c.get("url"):
                    allow.add(c["url"])
        if verdict == "verified" and n_verified == 0:
            fails.append("fact %r: marked verified but no citation is "
                         "verified" % fid)
        if verdict == "failed":
            fails.append("fact %r: FAILED verification — remove it from the "
                         "working set before writing" % fid)
        if verdict == "unreachable" and n_verified == 0:
            fails.append("fact %r: unreachable with no verified citation — "
                         "treat as failed" % fid)

    print("verification-gate · %s · facts: %d verified / %d failed / %d "
          "unreachable" % (args.manifest.name, counts["verified"],
                           counts["failed"], counts["unreachable"]))
    for f in fails:
        print("  FAIL " + f)
    if fails:
        print("FAILED (%d issue(s))" % len(fails))
        return 1
    for u in sorted(allow):
        print("ALLOW " + u)
    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
