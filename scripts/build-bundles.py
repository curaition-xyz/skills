#!/usr/bin/env python3
"""Build installable .zip bundles from the skills in this repo.

Claude uploads one skill per .zip, and the zip must contain the skill FOLDER at
its root. A packaged skill therefore has no siblings — which is a problem for
the shared voice guide in `skills/_voice/`, since in the repo the chain skills
reach it as `../_voice/`.

So this script copies `_voice/` INTO each chain skill's bundle. The repo keeps
one canonical copy; the distributable carries a copy per bundle. Single source,
built distribution — edit `skills/_voice/`, rebuild, and every bundle updates.
The skills themselves check `_voice/` inside first, then `../_voice/` beside, so
the same SKILL.md works in both layouts.

Usage:
    python3 scripts/build-bundles.py            # build everything into dist/
    python3 scripts/build-bundles.py --check    # verify only, build nothing
"""

from __future__ import annotations

import argparse
import shutil
import sys
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKILLS = REPO / "skills"
DIST = REPO / "dist"

# Skills that resolve the shared voice guide. Everything else ships as-is:
# the Gymshark skills and digest carry their own client/product voice by design.
VOICE_CONSUMERS = {
    "cultural-scout",
    "click-bait-scout",
    "user-needs-classifier",
    "story-packager",
    "linkedin-writer",
    "substack-writer",
}

# Directories under skills/ that are shared resources, not skills.
NOT_A_SKILL = {"_voice"}

EXCLUDE = {".DS_Store", "__pycache__", ".pytest_cache"}


def skill_dirs() -> list[Path]:
    return sorted(
        d
        for d in SKILLS.iterdir()
        if d.is_dir() and d.name not in NOT_A_SKILL and not d.name.startswith(".")
    )


def check() -> list[str]:
    """Return a list of problems. Empty list means the tree is publishable."""
    problems = []
    voice = SKILLS / "_voice"

    if not (voice / "curaition-tone-of-voice.md").is_file():
        problems.append("skills/_voice/curaition-tone-of-voice.md is missing")

    for d in skill_dirs():
        if not (d / "SKILL.md").is_file():
            problems.append(f"{d.name}/ has no SKILL.md — Claude will reject the zip")
            continue
        head = (d / "SKILL.md").read_text(encoding="utf-8").lstrip()
        if not head.startswith("---"):
            problems.append(f"{d.name}/SKILL.md does not start with YAML frontmatter")
        elif f"name: {d.name}" not in head.split("---")[1]:
            problems.append(
                f"{d.name}/SKILL.md frontmatter name does not match its folder name"
            )
    return problems


def build_one(src: Path, out: Path) -> tuple[int, bool]:
    """Zip one skill. Returns (file count, whether the voice guide was folded in)."""
    staged = DIST / "_staging" / src.name
    if staged.exists():
        shutil.rmtree(staged)
    staged.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(
        src, staged, ignore=shutil.ignore_patterns(*EXCLUDE)
    )

    bundled_voice = src.name in VOICE_CONSUMERS
    if bundled_voice:
        shutil.copytree(
            SKILLS / "_voice",
            staged / "_voice",
            ignore=shutil.ignore_patterns(*EXCLUDE),
        )

    count = 0
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(staged.rglob("*")):
            if f.is_file():
                # arcname keeps the skill folder as the zip root, as Claude requires.
                z.write(f, Path(src.name) / f.relative_to(staged))
                count += 1
    shutil.rmtree(staged)
    return count, bundled_voice


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="verify only, build nothing")
    args = ap.parse_args()

    problems = check()
    if problems:
        print("FAILED — fix these before building:\n")
        for p in problems:
            print(f"  · {p}")
        return 1

    if args.check:
        print(f"OK — {len(skill_dirs())} skills are publishable.")
        return 0

    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()

    print(f"Building into {DIST.relative_to(REPO)}/\n")
    for d in skill_dirs():
        out = DIST / f"{d.name}.zip"
        count, voiced = build_one(d, out)
        size = out.stat().st_size / 1024
        tag = "  + voice guide" if voiced else ""
        print(f"  {d.name:<26} {count:>3} files  {size:>7.1f} KB{tag}")

    staging = DIST / "_staging"
    if staging.exists():
        shutil.rmtree(staging)

    print(f"\n{len(skill_dirs())} bundles ready. Upload these .zip files to Claude.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
