#!/usr/bin/env python3
"""
CurAItion writer voice lint — the "validate, don't hope" gate for the channel
writers in the editorial chain. Encodes the mechanical half of the canonical
publishing spec (GBrain `curaition/daily-publishing-prompt`, 16 Aug 2026)
plus the tone-of-voice guide. Passing the lint is necessary, never
sufficient.

Channels: linkedin | substack-drop | ig-caption | first-comment

HARD failures (exit 1), all channels:
  - em dash (—) anywhere in the body
  - double hyphen (--) anywhere in the body (URLs inside markdown links are
    excluded from this check)
  - US spelling (colour not color, realise not realize, …)
  - a filler opener
  - word count outside the channel band

Channel-specific HARD failures:
  substack-drop:
  - a trailing sources block ("Sources: …") — sources are inline links only
  - no subtitle (every issue requires one: title opens the gap, subtitle
    hints at the answer without resolving it)
  linkedin:
  - does not end with "Full breakdown in the comments" (hashtags may follow)
  - more than 3 hashtags, or missing #CulturalIntelligence / #BrandStrategy
  - first line differs from the Drop subtitle (when --drop is supplied)
  ig-caption:
  - more than one line, or does not end with an emoji
  first-comment:
  - no substack.com link, or missing #curaition

WARN (exit 0, printed for review):
  - a number in the draft not traceable to the package facts[] (--package)
  - a sentence over ~40 words
  - three or more consecutive short sentences of similar length (parallel
    structure — reads as constructed, not discovered)

Usage:
    python voice_lint.py DRAFT.md --channel linkedin|substack-drop|ig-caption|first-comment \
        [--package story-package.json] [--drop substack-draft.md]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# channel word-count bands (min, max)
BANDS = {
    "linkedin": (140, 260),        # tone doc: 150-250, small grace either side
    "substack-drop": (400, 1000),  # canonical: 1,000 words max
    "ig-caption": (3, 40),
    "first-comment": (2, 80),
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
MD_LINK = re.compile(r"\[([^\]]*)\]\(([^)\s]+)\)")
HASHTAG = re.compile(r"#\w+")
SOURCES_BLOCK = re.compile(r"^\s*\*?_?\s*sources?\s*:", re.I)
# emoji: anything outside the basic multilingual ASCII/latin planes at EOL
EMOJI_END = re.compile(r"[\U0001F000-\U0001FAFF☀-➿⬀-⯿]️?\s*$")


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
    s = MD_LINK.sub(r"\1", s)          # keep anchor text, drop URL
    s = re.sub(r"[#>*_`]", "", s)
    return s


def first_paragraph(lines: list[str]) -> str:
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


def drop_subtitle(drop_path: Path) -> str | None:
    """The Drop's subtitle: the first non-empty prose line after the H1."""
    seen_h1 = False
    for ln in drop_path.read_text(encoding="utf-8").splitlines():
        s = ln.strip()
        if not s or HR_LINE.match(ln) or META_LINE.match(ln):
            continue
        if s.startswith("# "):
            seen_h1 = True
            continue
        if seen_h1 and not s.startswith("#"):
            return strip_md(s).strip().strip("*_").strip()
    return None


def _norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def package_corpus(pkg: dict) -> str:
    facts = pkg.get("facts", [])
    return json.dumps(facts, ensure_ascii=False).lower()


NUM = re.compile(r"\d[\d,]*(?:\.\d+)?")


def norm_num(tok: str) -> str:
    return tok.replace(",", "").rstrip(".")


def check(draft_path: Path, channel: str, pkg: dict | None,
          drop_path: Path | None):
    text = draft_path.read_text(encoding="utf-8")
    lines = body_lines(text, channel)
    body = "\n".join(lines)
    body_no_urls = MD_LINK.sub(lambda m: "[%s](URL)" % m.group(1), body)
    fails, warns = [], []

    # 1. em dash
    if "—" in body:
        n = body.count("—")
        fails.append(f"em dash (—) appears {n}× — replace with a full stop or comma")

    # 2. double hyphen (canonical: no double hyphens. Anywhere.)
    if "--" in body_no_urls:
        n = body_no_urls.count("--")
        fails.append(f"double hyphen (--) appears {n}× — replace with a full stop or comma")

    # 3. US spelling
    words = re.findall(r"[A-Za-z']+", strip_md(body).lower())
    hits = sorted({w for w in words if w in US_SPELLINGS})
    if hits:
        fails.append("US spelling: " + ", ".join(hits) + " (use British English)")

    # 4. filler opener
    op = first_paragraph(lines).lower()
    for pat in FILLER_OPENERS:
        if re.match(r"\s*" + pat, op):
            fails.append(f"filler opener: draft starts '{op[:60]}…' — just start with the thing")
            break

    # 5. word count
    wc = len(re.findall(r"\b[\w']+\b", strip_md(body)))
    lo, hi = BANDS.get(channel, (0, 10**9))
    if wc < lo or wc > hi:
        fails.append(f"word count {wc} outside {channel} band {lo}–{hi}")

    prose = strip_md(body)

    # 6. channel-specific contracts
    if channel == "substack-drop":
        # trailing sources block is banned — sources are inline links only
        tail = [ln for ln in lines if ln.strip()][-4:]
        for ln in tail:
            if SOURCES_BLOCK.match(ln):
                fails.append("trailing sources block — the Drop carries "
                             "sources as inline links only")
                break
        sub = drop_subtitle(draft_path)
        if not sub:
            fails.append("no subtitle — every issue requires one (title "
                         "opens the gap, subtitle hints without resolving)")
        if not MD_LINK.search(body):
            warns.append("no inline links — the Drop hyperlinks its sources "
                         "in the body")

    if channel == "linkedin":
        tags = HASHTAG.findall(body)
        content_wo_tags = strip_md(HASHTAG.sub("", body)).rstrip().rstrip(".")
        if not content_wo_tags.lower().endswith("full breakdown in the comments"):
            fails.append('does not end with "Full breakdown in the comments"')
        if len(tags) > 3:
            fails.append("%d hashtags — maximum 3 "
                         "(#CulturalIntelligence #BrandStrategy + one variable)"
                         % len(tags))
        if tags:
            low = {t.lower() for t in tags}
            for req in ("#culturalintelligence", "#brandstrategy"):
                if req not in low:
                    fails.append("missing required hashtag %s" % req)
        else:
            warns.append("no hashtags — canonical is #CulturalIntelligence "
                         "#BrandStrategy + one variable")
        if drop_path is not None:
            sub = drop_subtitle(drop_path)
            first = next((strip_md(ln).strip() for ln in lines if ln.strip()), "")
            if sub is None:
                warns.append("--drop supplied but no subtitle found in it")
            elif _norm(first) != _norm(sub):
                fails.append("first line differs from the Drop subtitle:\n"
                             "         post:  %s\n         drop:  %s"
                             % (first[:70], sub[:70]))
        else:
            warns.append("no --drop supplied: subtitle-mirror contract not checked")

    if channel == "ig-caption":
        content_lines = [ln for ln in lines if ln.strip()]
        if len(content_lines) != 1:
            fails.append("caption must be exactly one line (found %d)"
                         % len(content_lines))
        if content_lines and not EMOJI_END.search(content_lines[-1]):
            fails.append("caption must end with a relevant emoji")

    if channel == "first-comment":
        if "substack.com" not in body:
            fails.append("no Substack link — the first comment carries the "
                         "full-story link")
        low = {t.lower() for t in HASHTAG.findall(body)}
        for req in ("#culturalintelligence", "#brandstrategy", "#curaition"):
            if req not in low:
                fails.append("missing required hashtag %s" % req)

    # 7. sentence length + parallel structure (warn)
    sents = [s for s in re.split(r"(?<=[.!?])\s+", prose) if s.strip()]
    for sent in sents:
        n = len(sent.split())
        if n > 40:
            warns.append(f"long sentence ({n} words): '{sent[:60]}…'")
    run = 0
    for a, b in zip(sents, sents[1:]):
        la, lb = len(a.split()), len(b.split())
        if la <= 8 and lb <= 8 and abs(la - lb) <= 1:
            run += 1
            if run == 2:
                warns.append("three consecutive short sentences of matched "
                             "length ('%s…') — parallel structure reads as "
                             "constructed, vary the rhythm" % a[:40])
        else:
            run = 0

    # 8. number fidelity vs facts[] (warn)
    if pkg is not None:
        corpus_clean = package_corpus(pkg).replace(",", "")
        seen = set()
        for tok in NUM.findall(prose):
            v = norm_num(tok)
            if len(v.replace(".", "")) >= 2 and v not in corpus_clean and v not in seen:
                seen.add(v)
                warns.append(f"number '{tok}' not found in package facts[] — verify it is not fabricated")
    elif channel in ("linkedin", "substack-drop"):
        warns.append("no --package supplied: fact/number fidelity not checked")

    return wc, fails, warns


def main() -> int:
    ap = argparse.ArgumentParser(description="CurAItion writer voice lint.")
    ap.add_argument("draft", type=Path)
    ap.add_argument("--channel", required=True, choices=sorted(BANDS))
    ap.add_argument("--package", type=Path, default=None)
    ap.add_argument("--drop", type=Path, default=None,
                    help="the rendered Drop draft (linkedin: checks the "
                         "first line mirrors its subtitle)")
    args = ap.parse_args()

    pkg = None
    if args.package:
        pkg = json.loads(args.package.read_text(encoding="utf-8"))

    wc, fails, warns = check(args.draft, args.channel, pkg, args.drop)
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
