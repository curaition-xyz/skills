#!/usr/bin/env python3
"""
CurAItion carousel density lint — the mechanical gate for slide copy.

Encodes GBrain `curaition/carousel-slide-density` (15 Aug 2026, backed by
reach data from @curai.tion Jul-Aug 2026) and the canonical publishing
spec. Run on the carousel.json BEFORE rendering; run again after any
slide edit.

HARD failures (exit 1):
  - any content slide with more than 3 lines
  - slide 1 (the hook) with more than 2 lines
  - a widow: last line of a slide 6 characters or fewer
    (the renderer would auto-merge it, but the merge may then break the
     3-line or length rules — fix the copy instead)
  - more than one chart slide
  - final slide missing or not last
  - em dash or double hyphen anywhere in slide copy

WARN (exit 0, printed for review):
  - content slide count differs from 8 (canonical deck is 8 + final)
  - a line longer than 24 characters (wraps at 66px — the rendered break
    then differs from the authored break, and visual line count drifts)
  - a 3-line slide (allowed, but "the best slides are 1-2 lines")
  - slide 1 opens with a question ("feels like an ad")
  - parallel structure: consecutive slides with near-identical line counts
    and lengths (reads as constructed, not discovered)

Usage:
    python slide_lint.py carousel.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

MAX_LINES = 3
HOOK_MAX_LINES = 2
WIDOW_CHARS = 6
LINE_LENGTH_WARN = 24
CANONICAL_CONTENT_COUNT = 8


def lint(deck: dict):
    fails, warns = [], []
    slides = deck.get("slides", [])
    content_like = [s for s in slides
                    if s.get("type", "content") in ("content", "chart")]
    charts = [s for s in slides if s.get("type") == "chart"]
    finals = [s for s in slides if s.get("type") == "final"]

    n_content = len(content_like)  # chart counts as a content slide
    if n_content != CANONICAL_CONTENT_COUNT:
        warns.append("deck has %d content slides (canonical is %d + final; "
                     "the chart counts as one)"
                     % (n_content, CANONICAL_CONTENT_COUNT))
    if len(charts) > 1:
        fails.append("%d chart slides — one maximum" % len(charts))
    if not finals:
        fails.append("no final brand slide")
    elif slides[-1].get("type") != "final":
        fails.append("final slide is not last")

    hook_seen = False
    prev_shape = None
    parallel_run = 0
    for idx, s in enumerate(slides, start=1):
        if s.get("type", "content") != "content":
            prev_shape = None
            continue
        copy = s.get("copy", "")
        lines = [ln for ln in copy.split("\n") if ln.strip()]
        tag = "slide %d" % idx

        if "—" in copy:
            fails.append("%s: em dash in copy" % tag)
        if "--" in copy:
            fails.append("%s: double hyphen in copy" % tag)

        if not hook_seen:
            hook_seen = True
            if len(lines) > HOOK_MAX_LINES:
                fails.append(
                    "%s (hook): %d lines — the hook is the sparest slide, "
                    "1-2 lines. If it needs a third line, split the slide."
                    % (tag, len(lines)))
            first = lines[0].strip() if lines else ""
            if first.endswith("?"):
                warns.append("%s (hook): opens with a question — the density "
                             "reference flags this as reading like an ad"
                             % tag)
        elif len(lines) > MAX_LINES:
            fails.append("%s: %d lines — maximum 3, ideally 2" %
                         (tag, len(lines)))
        elif len(lines) == MAX_LINES:
            warns.append("%s: 3 lines — allowed, but the best slides are "
                         "1-2. Does each line do something the previous "
                         "one doesn't?" % tag)

        if lines and 0 < len(lines[-1].strip()) <= WIDOW_CHARS:
            fails.append("%s: widow ('%s') — merge or rewrite the break"
                         % (tag, lines[-1].strip()))
        for ln in lines:
            if len(ln) > LINE_LENGTH_WARN:
                warns.append("%s: line %d chars ('%s…') — wraps at 66px; "
                             "rebreak so authored lines are rendered lines"
                             % (tag, len(ln), ln[:24]))

        shape = (len(lines), tuple(len(ln) // 8 for ln in lines))
        if shape == prev_shape:
            parallel_run += 1
            if parallel_run >= 2:
                warns.append("%s: third consecutive slide with the same "
                             "line shape — parallel structure reads as "
                             "constructed" % tag)
        else:
            parallel_run = 0
        prev_shape = shape

    return fails, warns


def main() -> int:
    ap = argparse.ArgumentParser(description="CurAItion carousel density lint.")
    ap.add_argument("carousel_json", type=Path)
    args = ap.parse_args()

    deck = json.loads(args.carousel_json.read_text(encoding="utf-8"))
    fails, warns = lint(deck)

    print("slide-lint · %s · %d slides" %
          (args.carousel_json.name, len(deck.get("slides", []))))
    for w in warns:
        print("  WARN " + w)
    for f in fails:
        print("  FAIL " + f)
    if fails:
        print("FAILED (%d hard issue(s))" % len(fails))
        return 1
    print("PASS (%d warning(s))" % len(warns))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
