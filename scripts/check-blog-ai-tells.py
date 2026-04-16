#!/usr/bin/env python3
"""Detect AI-written content patterns in blog posts.

Blocks commit if AI tells are found. Designed for pre-commit hook use.

Usage:
    python3 check-blog-ai-tells.py [install|--no-install] [paths...]

With no args: scans all staged .md/.astro/.mdx files.
With 'install' arg: symlinks this script as .git/hooks/pre-commit.
With paths: scans those specific files.
"""

import os
import re
import sys


PATTERNS = {
    "VAGUE_FILLER": [
        r"\bplays a role in\b",
        r"\bcrucial for\b",
        r"\bessential for\b",
        r"\bvital for\b",
        r"\bsignificant milestone\b",
        r"\beverlasting impact\b",
        r"\btimeless appeal\b",
        r"\benduring legacy\b",
        r"\bfoundation for\b",
        r"\bpillar of\b",
        r"\benhances?\b",
        r"\bdelves? into\b",
        r"\bembarks? on\b",
        r"\bembark on a (journey|quest|adventure)\b",
        r"\btrek through\b",
        r"\bleverages?\b",
        r"\bempowers?\b",
        r"\bspearheads?\b",
    ],
    "THESAURUS_PROSE": [
        r"\bvibrant\b",
        r"\bbustling\b",
        r"\bbreathtaking\b",
        r"\bcaptivates?\b",
        r"\billustrious\b",
        r"\brenowned\b",
        r"\bprofound impact\b",
        r"\bsuperlative\b",
        r"\bunparalleled\b",
        r"\bmultifaceted\b",
        r"\bintricately (crafted|designed|woven)\b",
        r"\bexpansive\b",
        r"\bencompassing\b",
        r"\bsignificance\b",
        r"\bpinnacle\b",
    ],
    "FORMULAIC_TRANSITIONS": [
        r"\bFirst and foremost\b",
        r"\bSecondly\b",
        r"\bIn conclusion\b",
        r"\bAdditionally\b",
        r"\bIn summary\b",
        r"\bFurthermore\b",
        r"\bMoreover\b",
        r"\bIn other words\b",
        r"\bThat being said\b",
        r"\bHaving said that\b",
        r"\bIt is worth noting\b",
        r"\bIt is important to note\b",
        r"\bTo that end\b",
        r"\bTo this end\b",
        r"\bat the end of the day\b",
        r"\ball things considered\b",
        r"\btake a dive\b",
        r"\btakes? a deep dive\b",
        r"\bdive (deep|into)\b",
    ],
    "HEDGING_WITHOUT_VALUE": [
        r"\bseems? to\b",
        r"\bsuggests? that\b",
        r"\bmay potentially\b",
        r"\bit appears that\b",
        r"\bone might say\b",
        r"\boftentimes\b",
        r"\boften times\b",
        r"\bbear? witness\b",
        r"\bserves? as a\b",
        r"\bcan be (seen as|considered|described as)\b",
        r"\bit could be argued\b",
    ],
    "PASSIVE_VOICE": [
        r"\bit was determined that\b",
        r"\bhas been developed by\b",
        r"\bcan be seen as\b",
        r"\bit was concluded that\b",
        r"\bwas (developed|created|built) by\b",
        r"\bis (being )?developed\b",
        r"\bhas been (shown|demonstrated|proven)\b",
        r"\bis (widely |generally )?considered\b",
        r"\bis (often |frequently )?referred to as\b",
        r"\bis (typically |commonly )?used (for|as|in)\b",
        r"\bhas (been )?widely (been )?adopted\b",
    ],
}

EXTS = (".md", ".mdx", ".astro")


def scan_file(path):
    """Scan a single file for AI tells. Returns list of (line, category, match)."""
    if not os.path.isfile(path):
        return []
    if not path.endswith(EXTS):
        return []
    try:
        lines = open(path, "r", encoding="utf-8", errors="replace").readlines()
    except Exception:
        return []

    hits = []
    for lineno, line in enumerate(lines, 1):
        for category, patterns in PATTERNS.items():
            for pat in patterns:
                if re.search(pat, line, re.IGNORECASE):
                    match = re.search(pat, line, re.IGNORECASE).group()
                    hits.append((lineno, category, match.strip()))
    return hits


def scan_paths(paths):
    """Scan a list of file paths. Returns dict of {path: [(line, cat, match), ...]}."""
    results = {}
    for p in paths:
        hits = scan_file(p)
        if hits:
            results[p] = hits
    return results


def install_hook():
    """Symlink this script as .git/hooks/pre-commit."""
    script = os.path.realpath(__file__)
    hook_dir = os.path.join(os.getcwd(), ".git", "hooks")
    hook_path = os.path.join(hook_dir, "pre-commit")
    os.makedirs(hook_dir, exist_ok=True)
    if os.path.islink(hook_path):
        os.remove(hook_path)
    elif os.path.isfile(hook_path):
        print(f"WARNING: {hook_path} already exists as a file — not installing hook")
        return
    os.symlink(script, hook_path)
    print(f"Installed pre-commit hook: {hook_path}")
    print("AI tells check will run on every commit.")


def get_staged_files():
    """Return list of staged .md/.mdx/.astro files via git."""
    import subprocess
    try:
        out = subprocess.check_output(
            ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
            text=True,
        )
        return [f.strip() for f in out.splitlines() if f.endswith(EXTS)]
    except subprocess.CalledProcessError:
        return []


def main():
    args = sys.argv[1:]

    # Handle install early (before file-scanning logic)
    if args and args[0] == "install":
        install_hook()
        return

    # Determine which files to scan
    if len(args) > 0 and args[0] == "--no-install":
        # --no-install means skip the auto-scan (for explicit runs)
        paths = args[1:] if len(args) > 1 else []
    elif args:
        paths = [a for a in args if os.path.isfile(a)]
    else:
        paths = get_staged_files()

    if not paths:
        print("No blog files staged or specified — allowing commit.")
        return

    results = scan_paths(paths)
    if not results:
        print(f"Scanned {len(paths)} file(s) — clean.")
        return

    # Print report and exit with error
    print("AI TELL(S) DETECTED — fix before committing:\n")
    for path, hits in results.items():
        print(f"  {path}")
        for lineno, cat, match in hits:
            print(f"    L{lineno}: [{cat}] \"{match}\"")
    print("\nEdit the flagged lines, then re-stage and commit.")
    print("Bypass: git commit --no-verify (use sparingly)")
    sys.exit(1)


if __name__ == "__main__":
    main()