#!/usr/bin/env python3
"""
Render a Drop markdown draft into paste-ready HTML for the Substack editor.

Why: pasting raw markdown into Substack loses every element (links, bold,
headings). Pasting RENDERED HTML from a browser keeps them — Substack's
editor accepts rich-text paste. This script produces a minimal HTML file:
open it in a browser, select all, copy, paste into the Substack body.

What it strips: the H1 title and the subtitle line. Those go into
Substack's own Title and Subtitle fields, not the body. Everything after
the subtitle is converted verbatim (pandoc), so inline links, bold, and
section headings survive the paste.

Usage:
    python drop_to_html.py <slug>-substack-drop.md
    → writes <slug>-substack-drop.html beside it, and prints the title and
      subtitle so they can be copied into Substack's fields.

Requires pandoc on PATH (preinstalled in the Cowork cloud container).
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

HR = re.compile(r"^\s*---\s*$")


def split_drop(text: str) -> tuple[str, str, str]:
    """Return (title, subtitle, body_md)."""
    lines = text.splitlines()
    title = ""
    subtitle = ""
    body_start = 0
    seen_title = False
    for i, ln in enumerate(lines):
        s = ln.strip()
        if not s or HR.match(ln):
            continue
        if not seen_title and s.startswith("# "):
            title = s[2:].strip()
            seen_title = True
            continue
        if seen_title and not subtitle and not s.startswith("#"):
            subtitle = s.strip().strip("*_").strip()
            body_start = i + 1
            break
    body = "\n".join(lines[body_start:]).strip()
    return title, subtitle, body


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    src = Path(sys.argv[1])
    text = src.read_text(encoding="utf-8")
    title, subtitle, body = split_drop(text)

    # House layout: the published Drop has NO H2/H3 headings in the body.
    # Sections are separated by horizontal rules and open with a bold
    # lead-in phrase. Demote any residual markdown headings to that form.
    demoted = []
    for ln in body.splitlines():
        m = re.match(r"^\s*#{2,}\s+(.*)$", ln)
        if m:
            lead = m.group(1).strip().rstrip(".")
            demoted.append("---")
            demoted.append("")
            demoted.append("**%s.**" % lead)
        else:
            demoted.append(ln)
    body = "\n".join(demoted)
    if not title or not subtitle:
        print("FAIL: could not find title (H1) and subtitle — is this a "
              "Drop draft?")
        return 1

    html_body = subprocess.run(
        ["pandoc", "-f", "markdown", "-t", "html"],
        input=body, capture_output=True, text=True, check=True,
    ).stdout

    out = src.with_suffix(".html")
    out.write_text(
        "<!doctype html><html><head><meta charset='utf-8'>"
        "<title>%s</title>"
        "<style>body{max-width:680px;margin:40px auto;"
        "font-family:Georgia,serif;font-size:18px;line-height:1.6}</style>"
        "</head><body>\n%s\n</body></html>\n" % (title, html_body),
        encoding="utf-8",
    )
    print("wrote", out)
    print("\nPaste these into Substack's own fields (they are NOT in the "
          "HTML body):")
    # house convention: the published title carries a terminal full stop
    print("  Title:    " + (title if title.endswith((".", "?", "!"))
                            else title + "."))
    print("  Subtitle: " + subtitle)
    print("\nThen open %s in a browser, select all, copy, and paste into "
          "the Substack body." % out.name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
