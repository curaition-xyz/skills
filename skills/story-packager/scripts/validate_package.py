#!/usr/bin/env python3
"""Validate a CurAItion Story Package.

Runs the JSON-Schema check plus the cross-field invariants that draft-07 cannot
express. Exit code 0 = pass (warnings allowed), 1 = at least one failure, 2 =
usage/IO error.

Usage:
    python validate_package.py PACKAGE.json
        [--schema references/story-package.schema.json]
        [--handoff story-candidate-<date>.json]     # enables citation-fidelity
        [--user-needs user-needs-<date>.json]        # enables carry-through check

The --handoff and --user-needs cross-checks are skipped (with a note) when the
files aren't supplied, so the script is useful both standalone and in the full
pipeline.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from urllib.parse import urlparse

CORE_BEATS = {"hook", "context", "tension", "depth", "why_now", "so_what", "cta"}
RESEARCH_SOURCES = {"CurAItion", "WebSearch", "WebFetch"}
AXIS = {
    "update_me": "know", "keep_me_engaged": "know",
    "give_me_perspective": "understand", "educate_me": "understand",
    "inspire_me": "feel", "divert_me": "feel",
    "help_me": "do", "connect_me": "do",
}


class Report:
    def __init__(self) -> None:
        self.fails: list[str] = []
        self.warns: list[str] = []
        self.notes: list[str] = []

    def fail(self, m: str) -> None: self.fails.append(m)
    def warn(self, m: str) -> None: self.warns.append(m)
    def note(self, m: str) -> None: self.notes.append(m)

    def emit(self, pkg_name: str) -> int:
        for m in self.notes: print(f"  · {m}")
        for m in self.warns: print(f"  ⚠ WARN  {m}")
        for m in self.fails: print(f"  ✗ FAIL  {m}")
        ok = not self.fails
        print(f"{'PASS' if ok else 'FAIL'}: {pkg_name} "
              f"({len(self.fails)} failures, {len(self.warns)} warnings)")
        return 0 if ok else 1


def load(p: str) -> dict:
    return json.loads(Path(p).read_text())


def schema_check(pkg: dict, schema_path: Path, r: Report) -> None:
    try:
        from jsonschema import Draft7Validator
    except ImportError:
        r.warn("jsonschema not installed — skipping schema validation "
               "(pip install jsonschema --break-system-packages)")
        return
    schema = json.loads(schema_path.read_text())
    Draft7Validator.check_schema(schema)
    for e in sorted(Draft7Validator(schema).iter_errors(pkg),
                    key=lambda e: list(e.path)):
        r.fail(f"schema: {list(e.path)} — {e.message}")


def collect_handoff_refs(handoff: dict) -> set[str]:
    """Every URL and content_id anywhere in the source handoff."""
    refs: set[str] = set()

    def walk(node):
        if isinstance(node, dict):
            for k, v in node.items():
                if k in ("url", "content_id", "evidence_url") and isinstance(v, str):
                    refs.add(v)
                else:
                    walk(v)
        elif isinstance(node, list):
            for v in node:
                walk(v)

    walk(handoff)
    return refs


def invariants(pkg: dict, r: Report, handoff: dict | None, user_needs: dict | None) -> None:
    facts = pkg.get("facts", [])
    fact_ids = {f["id"] for f in facts}

    # 1. facts: citations present + source restricted to research tools
    for f in facts:
        if not f.get("citations"):
            r.fail(f"fact {f['id']} has no citation")
        if f.get("source") not in RESEARCH_SOURCES:
            r.fail(f"fact {f['id']} source '{f.get('source')}' is not a research "
                   f"tool (facts may never be sourced to a pipeline stage)")

    # 2. narrative spine: beat_type <-> supports, and supports ⊆ facts
    for b in pkg.get("editorial", {}).get("narrative_spine", []):
        bt = b.get("beat_type", "grounded")
        sup = b.get("supports", [])
        beat = b.get("beat", "?")
        if bt == "grounded" and not sup:
            r.fail(f"grounded beat '{beat}' has no supports")
        if bt in ("lift", "structural") and sup:
            r.fail(f"{bt} beat '{beat}' must not carry supports")
        for fid in sup:
            if fid not in fact_ids:
                r.fail(f"beat '{beat}' supports '{fid}' which is not in facts[]")
        if beat not in CORE_BEATS:
            r.warn(f"beat '{beat}' is outside the core vocabulary "
                   f"{sorted(CORE_BEATS)} (allowed, but writers can't rely on it)")

    # 3. assets: ephemeral origins must be flagged for rehost; embeds need providers
    for a in pkg.get("assets", []):
        if a.get("origin") in ("replicate",) or a.get("durable") is False:
            if not a.get("rehost_required"):
                r.fail(f"asset {a.get('id')} is non-durable but not flagged "
                       f"rehost_required")
        if a.get("kind") == "embed" and not a.get("embed_provider"):
            r.warn(f"embed asset {a.get('id')} has no embed_provider")

    # 4. click-bait two-source rule on the core claim
    if pkg.get("source", {}).get("mode") == "click-bait":
        sig = [f for f in facts if f.get("layer") == "signal_24h"]
        if sig:
            top = max(f["importance"] for f in sig)
            leads = [f for f in sig if f["importance"] == top]
            corroborated = any(
                len({(c.get("outlet") or urlparse(c.get("url", "")).netloc)
                     for c in f["citations"]}) >= 2
                for f in leads
            )
            if not corroborated:
                r.fail("click-bait: no lead signal_24h fact has 2+ independent "
                       "outlets (two-source rule)")

    # 5. citation fidelity (needs the handoff)
    if handoff is not None:
        refs = collect_handoff_refs(handoff)
        for f in facts:
            for c in f["citations"]:
                ref = c.get("url") or c.get("content_id")
                if ref and ref not in refs:
                    r.fail(f"fact {f['id']} cites '{ref}' which is absent from the "
                           f"handoff (citation fidelity: no new sources)")
    else:
        r.note("citation-fidelity check skipped (no --handoff supplied)")

    # 6. carry-through (needs the user-needs file)
    src = pkg.get("source", {})
    tone = pkg.get("editorial", {}).get("tone", {})
    if user_needs is not None:
        sel = user_needs.get("selected_candidate_id")
        cls = next((c for c in user_needs.get("classifications", [])
                    if c["candidate_id"] == sel), None)
        if cls is None:
            r.warn("user-needs file has no classification for its "
                   "selected_candidate_id")
        else:
            if tone.get("primary_need") != cls["primary_need"]:
                r.fail(f"carry-through: package need '{tone.get('primary_need')}' "
                       f"!= classifier '{cls['primary_need']}'")
            if any(b["field"].startswith("editorial.tone")
                   for b in pkg.get("backfill", [])):
                r.fail("carry-through: tone/need is in backfill even though a "
                       "user-needs file is present (should be carried, not derived)")
    elif src.get("user_needs_file"):
        r.warn("source names a user_needs_file but none supplied to the validator "
               "— carry-through not checked")
    else:
        r.note("carry-through check skipped (no user-needs file in play)")

    # 7. tone axis/need consistency
    pn, pa = tone.get("primary_need"), tone.get("primary_axis")
    if pn and pa and AXIS.get(pn) != pa:
        r.fail(f"tone primary_need '{pn}' is on axis '{AXIS.get(pn)}', not '{pa}'")

    # 8. format_readiness present (v1 expects it)
    if "format_readiness" not in pkg:
        r.warn("no format_readiness block — writers can't see the substance ceiling")


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate a CurAItion Story Package.")
    ap.add_argument("package")
    ap.add_argument("--schema", default=None)
    ap.add_argument("--handoff", default=None)
    ap.add_argument("--user-needs", default=None)
    args = ap.parse_args()

    schema_path = Path(args.schema) if args.schema else (
        Path(__file__).resolve().parent.parent / "references" / "story-package.schema.json")

    try:
        pkg = load(args.package)
        handoff = load(args.handoff) if args.handoff else None
        user_needs = load(args.user_needs) if args.user_needs else None
    except Exception as e:  # noqa: BLE001
        print(f"IO error: {e}", file=sys.stderr)
        return 2

    print(f"Validating {args.package}")
    r = Report()
    if schema_path.exists():
        schema_check(pkg, schema_path, r)
    else:
        r.warn(f"schema not found at {schema_path} — skipping schema validation")
    invariants(pkg, r, handoff, user_needs)
    return r.emit(Path(args.package).name)


if __name__ == "__main__":
    sys.exit(main())
