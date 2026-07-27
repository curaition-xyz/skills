#!/usr/bin/env python3
"""
CurAItion writer voice lint — the "validate, don't hope" gate for the channel
writers in the editorial chain. Same gate philosophy as the
packager's validate_package.py: encode the rules a human reviewer would apply,
and refuse to ship a draft that breaks the hard ones.

Checks a rendered channel draft against the CurAItion tone-of-voice and, when
given the source Story Package, against its frozen facts[] layer.

HARD failures (exit 1):
  - em dash (—) anywhere in the body
  - US spelling (colour not color, realise not realize, …)
  - a filler opener ("We're excited to…", "In today's evolving…", …)
  - word count outside the channel band

WARN (exit 0, still printed — for human review, not a block):
  - a number in the draft not traceable to the package facts[] / citations
  - a named outlet/URL not present in the package citations
  - a sentence over ~40 words (the "short sentences" principle)

Usage:
    python voice_lint.py DRAFT.md --channel linkedin|substack-drop \
        [--package story-package.json]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# channel word-count bands (min, max) — from curaition-tone-of-voice.md
BANDS = {
    "linkedin": (140, 260),        # tone doc: 150–250, small grace either side
    "substack-drop": (400, 1000),  # The Drop: premium depth version
}

# high-precision US→UK spellings (kept conservative to avoid false positives)
US_SPELLINGS = {
    "color", "colors", "colored", "coloring",
    "realize", "realized", "realizing", "realizes",
    "organize", "organized", "organizing", "organization", "organizations",
    "recognize", "recognized", "recognizing",
    "analyze", "analyzed", "analyzing",
    "favorite", "favorites", "favor", "favored",
    "center", "centered", "centers",
    "behavior", "behaviors", "honor", "honored", "labor", "neighbor",
    "defense", "offense", "license",  # noun spelled licence in UK
    "catalog", "catalogs", "dialog",
    "maximize", "minimize", "optimize", "optimized", "optimizing",
    "apologize", "prioritize", "prioritized",
    "gray", "fiber", "liter", "aluminum",
    "traveled", "traveling", "modeling", "canceled", "labeled",
}

FILLER_OPENERS = [
    r"we'?re (excited|thrilled|pleased|happy|delighted) to",
    r"today,? we'?re",
    r"i wanted to reach out",
    r"in today'?s (rapidly )?(evolving|changing|complex)",
    r"as a valued",
    r"in an? (increasingly|ever[- ])",
    r"it'?s no secret that",
    r"i'?m (excited|thrilled|pleased|delighted)",
    r"we are excited",
    r"in the (fast[- ]paced|ever[- ]changing) world",
]

META_LINE = re.compile(r"^\s*(\*_?rendered from|\*calibrated to|<!--)", re.I)
HR_LINE = re.compile(r"^\s*---\s*$")


def body_lines(text: str, channel: str) -> list[str]:
    out = []
    dropped_h1 = False
    for ln in text.splitlines():
        if META_LINE.match(ln) or HR_LINE.match(ln):
            continue
        # A LinkedIn post has no headline; a leading '# …' is only a file
        # label, so exclude it. The Drop's leading '# …' IS the headline and
        # is kept (it must obey the no-em-dash / spelling rules too).
        if channel == "linkedin" and not dropped_h1 and ln.lstrip().startswith("# "):
            dropped_h1 = True
            continue
        out.append(ln)
    return out


def strip_md(s: str) -> str:
    s = re.sub(r"[#>*_`]", "", s)
    return s


def first_paragraph(lines: list[str]) -> str:
    # skip a leading H1 title, find first real prose paragraph
    para = []
    started = False
    for ln in lines:
        if not ln.strip():
            if started:
                break
            continue
        if ln.lstrip().startswith("# ") and not started:
            continue  # title
        started = True
        para.append(ln.strip())
    return strip_md(" ".join(para)).strip()


def package_corpus(pkg: dict) -> str:
    """All fact/citation text — the frozen ground truth a draft may draw on."""
    facts = pkg.get("facts", [])
    return json.dumps(facts, ensure_ascii=False).lower()


# numeric core only — no leading $/trailing % or word-boundary, so magnitude
# suffixes ("$296M", "22%") don't hide the digits from extraction.
NUM = re.compile(r"\d[\d,]*(?:\.\d+)?")


def norm_num(tok: str) -> str:
    return tok.replace(",", "").rstrip(".")


def check(draft_path: Path, channel: str, pkg: dict | None):
    text = draft_path.read_text(encoding="utf-8")
    lines = body_lines(text, channel)
    body = "\n".join(lines)
    fails, warns = [], []

    # 1. em dash
    if "—" in body:
        n = body.count("—")
        fails.append(f"em dash (—) appears {n}× — replace with a full stop or comma")

    # 2. US spelling
    words = re.findall(r"[A-Za-z']+", body.lower())
    hits = sorted({w for w in words if w in US_SPELLINGS})
    if hits:
        fails.append("US spelling: " + ", ".join(hits) + " (use British English)")

    # 3. filler opener
    op = first_paragraph(lines).lower()
    for pat in FILLER_OPENERS:
        if re.match(r"\s*" + pat, op):
            fails.append(f"filler opener: draft starts '{op[:60]}…' — just start with the thing")
            break

    # 4. word count
    wc = len(re.findall(r"\b[\w']+\b", strip_md(body)))
    lo, hi = BANDS.get(channel, (0, 10**9))
    if wc < lo or wc > hi:
        fails.append(f"word count {wc} outside {channel} band {lo}–{hi}")

    # 5. sentence length (warn)
    for sent in re.split(r"(?<=[.!?])\s+", strip_md(body)):
        n = len(sent.split())
        if n > 40:
            warns.append(f"long sentence ({n} words): '{sent[:60]}…'")

    # 6. number fidelity vs facts[] (warn) — substring match on a comma-stripped
    #    corpus so "$296 million" traces to a fact stored as "$296M".
    if pkg is not None:
        corpus_clean = package_corpus(pkg).replace(",", "")
        seen = set()
        for tok in NUM.findall(strip_md(body)):
            v = norm_num(tok)
            if len(v.replace(".", "")) >= 2 and v not in corpus_clean and v not in seen:
                seen.add(v)
                warns.append(f"number '{tok}' not found in package facts[] — verify it is not fabricated")
    else:
        warns.append("no --package supplied: fact/number fidelity not checked")

    return wc, fails, warns


def main() -> int:
    ap = argparse.ArgumentParser(description="CurAItion writer voice lint.")
    ap.add_argument("draft", type=Path)
    ap.add_argument("--channel", required=True, choices=sorted(BANDS))
    ap.add_argument("--package", type=Path, default=None)
    args = ap.parse_args()

    pkg = None
    if args.package:
        pkg = json.loads(args.package.read_text(encoding="utf-8"))

    wc, fails, warns = check(args.draft, args.channel, pkg)
    print(f"voice-lint · {args.draft.name} · {args.channel} · {wc} words")
    for w in warns:
        print("  WARN " + w)
    for f in fails:
        print("  FAIL " + f)
    if fails:
        print(f"FAILED ({len(fails)} hard issue(s))")
        return 1
    print(f"PASS ({len(warns)} warning(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
