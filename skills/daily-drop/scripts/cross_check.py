#!/usr/bin/env python3
"""
Daily Drop cross-asset gate — Stage 6 of the daily publishing run.

Mechanical assertions ACROSS the day's assets. Per-asset voice rules are the
voice lint's job (`_voice/voice_lint.py`); slide density is the carousel
lint's job (`carousel-producer/scripts/slide_lint.py`). This script owns the
contracts BETWEEN assets:

HARD failures (exit 1):
  - LinkedIn post first line != the Drop's subtitle (verbatim, whitespace-
    and punctuation-normalised)
  - LinkedIn post does not end "Full breakdown in the comments" (hashtags
    may follow)
  - a link in any draft that is not on the verified allowlist
    (verification-<date>.json)
  - the Drop over 1,000 words, missing a subtitle, or carrying a trailing
    sources block
  - an em dash or double hyphen in any asset
  - IG caption not exactly one line, or not emoji-terminated
  - first comment missing the substack.com link or #curaition
  - carousel.json fails the density rules bundled here (>3 lines, hook >2
    lines, widow, >1 chart, final not last)

Usage:
    python cross_check.py daily-drafts/<date>/ --slug <slug>
    (expects <slug>-substack-drop.md, <slug>-linkedin.md,
     <slug>-linkedin-first-comment.md, <slug>-ig-caption.md,
     carousel-<slug>.json, verification-<date>.json in the directory)

Missing files are reported as failures — every asset is mandatory for a
publishable issue.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

MD_LINK = re.compile(r"\[([^\]]*)\]\(([^)\s]+)\)")
BARE_URL = re.compile(r"https?://[^\s)\]>\"']+")
HASHTAG = re.compile(r"#\w+")
SOURCES_BLOCK = re.compile(r"^\s*\*?_?\s*sources?\s*:", re.I)
HR_LINE = re.compile(r"^\s*---\s*$")
EMOJI_END = re.compile(r"[\U0001F000-\U0001FAFF☀-➿⬀-⯿]️?\s*$")


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def strip_md(s: str) -> str:
    s = MD_LINK.sub(r"\1", s)
    return re.sub(r"[#>*_`]", "", s)


def read_lines(p: Path) -> list[str]:
    return [ln for ln in p.read_text(encoding="utf-8").splitlines()
            if not HR_LINE.match(ln)]


def drop_subtitle(lines: list[str]) -> str | None:
    seen_h1 = False
    for ln in lines:
        s = ln.strip()
        if not s:
            continue
        if s.startswith("# "):
            seen_h1 = True
            continue
        if seen_h1 and not s.startswith("#"):
            return strip_md(s).strip().strip("*_").strip()
    return None


def urls_in(text: str) -> set[str]:
    urls = {m.group(2) for m in MD_LINK.finditer(text)}
    urls |= set(BARE_URL.findall(MD_LINK.sub(r"\1", text)))
    return urls


def dash_check(name: str, text: str, fails: list[str]) -> None:
    no_urls = MD_LINK.sub(lambda m: "[%s](URL)" % m.group(1), text)
    no_urls = BARE_URL.sub("URL", no_urls)
    if "—" in no_urls:
        fails.append("%s: em dash" % name)
    if "--" in no_urls:
        fails.append("%s: double hyphen" % name)


def check_carousel(deck: dict, fails: list[str]) -> None:
    slides = deck.get("slides", [])
    charts = [s for s in slides if s.get("type") == "chart"]
    if len(charts) > 1:
        fails.append("carousel: %d chart slides — one maximum" % len(charts))
    if not slides or slides[-1].get("type") != "final":
        fails.append("carousel: final brand slide missing or not last")
    hook_seen = False
    for idx, s in enumerate(slides, start=1):
        if s.get("type", "content") != "content":
            continue
        lines = [ln for ln in s.get("copy", "").split("\n") if ln.strip()]
        if not hook_seen:
            hook_seen = True
            if len(lines) > 2:
                fails.append("carousel slide %d (hook): %d lines — max 2"
                             % (idx, len(lines)))
        elif len(lines) > 3:
            fails.append("carousel slide %d: %d lines — max 3"
                         % (idx, len(lines)))
        if lines and 0 < len(lines[-1].strip()) <= 6:
            fails.append("carousel slide %d: widow ('%s')"
                         % (idx, lines[-1].strip()))
        dash_check("carousel slide %d" % idx, s.get("copy", ""), fails)


def main() -> int:
    ap = argparse.ArgumentParser(description="Daily Drop cross-asset gate.")
    ap.add_argument("staging", type=Path)
    ap.add_argument("--slug", required=True)
    args = ap.parse_args()
    d, slug = args.staging, args.slug
    fails = []

    paths = {
        "drop": d / f"{slug}-substack-drop.md",
        "linkedin": d / f"{slug}-linkedin.md",
        "comment": d / f"{slug}-linkedin-first-comment.md",
        "caption": d / f"{slug}-ig-caption.md",
        "carousel": d / f"carousel-{slug}.json",
    }
    verifs = sorted(d.glob("verification-*.json"))

    texts = {}
    for name, p in paths.items():
        if not p.exists():
            fails.append("missing asset: %s" % p.name)
        elif name != "carousel":
            texts[name] = p.read_text(encoding="utf-8")

    # allowlist
    allow: set[str] = set()
    if not verifs:
        fails.append("missing verification-<date>.json — the run has no "
                     "link allowlist")
    else:
        manifest = json.loads(verifs[-1].read_text(encoding="utf-8"))
        for f in manifest.get("facts", []):
            for c in f.get("citations", []):
                if c.get("status") == "verified" and c.get("url"):
                    allow.add(c["url"])

    # Drop contracts
    if "drop" in texts:
        lines = read_lines(paths["drop"])
        sub = drop_subtitle(lines)
        if not sub:
            fails.append("drop: no subtitle")
        wc = len(re.findall(r"\b[\w']+\b", strip_md(texts["drop"])))
        if wc > 1000:
            fails.append("drop: %d words — 1,000 max" % wc)
        tail = [ln for ln in lines if ln.strip()][-4:]
        if any(SOURCES_BLOCK.match(ln) for ln in tail):
            fails.append("drop: trailing sources block — inline links only")
        dash_check("drop", texts["drop"], fails)

        # LinkedIn mirror
        if "linkedin" in texts:
            li_lines = [ln for ln in read_lines(paths["linkedin"])
                        if ln.strip() and not ln.lstrip().startswith("# ")]
            first = strip_md(li_lines[0]).strip() if li_lines else ""
            if sub and norm(first) != norm(sub):
                fails.append("linkedin first line != drop subtitle:\n"
                             "         post: %s\n         drop: %s"
                             % (first[:70], (sub or "")[:70]))

    if "linkedin" in texts:
        body = texts["linkedin"]
        wo_tags = strip_md(HASHTAG.sub("", body)).rstrip().rstrip(".")
        if not wo_tags.lower().endswith("full breakdown in the comments"):
            fails.append('linkedin: does not end "Full breakdown in the '
                         'comments"')
        tags = HASHTAG.findall(body)
        if len(tags) > 3:
            fails.append("linkedin: %d hashtags — max 3" % len(tags))
        if urls_in(body):
            fails.append("linkedin: link in post body — links live in the "
                         "first comment")
        dash_check("linkedin", body, fails)

    if "comment" in texts:
        if "substack.com" not in texts["comment"]:
            fails.append("first comment: no substack.com link")
        low = {t.lower() for t in HASHTAG.findall(texts["comment"])}
        if "#curaition" not in low:
            fails.append("first comment: missing #curaition")
        dash_check("first comment", texts["comment"], fails)

    if "caption" in texts:
        content = [ln for ln in texts["caption"].splitlines() if ln.strip()]
        if len(content) != 1:
            fails.append("caption: must be exactly one line (found %d)"
                         % len(content))
        elif not EMOJI_END.search(content[0]):
            fails.append("caption: must end with a relevant emoji")
        dash_check("caption", texts["caption"], fails)

    if paths["carousel"].exists():
        check_carousel(json.loads(paths["carousel"].read_text(
            encoding="utf-8")), fails)

    # link allowlist across text assets (substack first-comment link exempt:
    # it points at the issue being published, not at a source)
    own_issue = re.compile(r"https?://curaition\.substack\.com/\S*")
    for name in ("drop", "linkedin", "caption"):
        if name not in texts:
            continue
        for u in urls_in(texts[name]):
            if own_issue.match(u):
                continue
            if u not in allow:
                fails.append("%s: link not on verified allowlist: %s"
                             % (name, u))

    print("cross-check · %s · slug %s" % (d, slug))
    for f in fails:
        print("  FAIL " + f)
    if fails:
        print("FAILED (%d issue(s))" % len(fails))
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
