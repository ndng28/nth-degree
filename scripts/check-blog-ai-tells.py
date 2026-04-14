#!/usr/bin/env python3
"""
Blog Post AI Tells Checker — pre-commit hook
==============================================
Checks staged markdown files for common AI writing patterns.
Based on: https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing

Usage:
    python3 check-blog-ai-tells.py file1.md file2.md ...

Exit codes:
    0 = clean, proceed with commit
    1 = AI tells found, commit blocked
    2 = usage error
"""

import sys
import re
import os

# Vague filler phrases — AI reaches for these instead of specific claims
VAGUE_FILLER = [
    (r"\bplays a role in\b", "vague: 'plays a role in' — be specific"),
    (r"\bcontributes to\b", "vague: 'contributes to' — be specific"),
    (r"\benduring legacy of\b", "AI tell: thesaurus phrase 'enduring legacy'"),
    (r"\bthe transformative power of\b", "AI tell: 'transformative power' — AI Wikipedia prose"),
    (r"\bthe significance of\b", "vague: 'significance of' — what specifically?"),
    (r"\benhances the (?!quality|performance|efficiency)\b", "vague: 'enhances' — be specific"),
    (r"\bfacilitates\b", "AI tell: 'facilitates' is formal AI-speak"),
    (r"\bleverages\b", "AI tell: 'leverages' is corporate AI-speak"),
    (r"\butilizes\b", "AI tell: 'utilizes' — use 'uses'"),
    (r"\bvital for\b", "vague: 'vital for' — why specifically?"),
    (r"\bimportant for\b", "vague: 'important for' — what is the actual consequence?"),
    (r"\bcrucial for\b", "vague: 'crucial for' — what happens without it?"),
    (r"\ba diverse range of\b", "AI tell: 'a diverse range of' — thesaurus filler"),
    (r"\ba wide range of\b", "AI tell: 'a wide range of' — be specific"),
    (r"\bvarious (factors|aspects|elements)\b", "vague: 'various factors' — name them"),
    (r"\bthe ecosystem\b", "overused: 'ecosystem' is AI tech-blog filler"),
    (r"\bcuts across\b", "AI tell: 'cuts across' — what does this actually mean?"),
    (r"\bdelves into\b", "AI tell: 'delves into' is AI article opener"),
    (r"\bnavigates the\b", "AI tell: 'navigates the' — be direct"),
    (r"\bencompasses\b", "AI tell: 'encompasses' is formal AI prose"),
    (r"\bserves as a\b", "AI tell: 'serves as a' — what is it?"),
    (r"\bin the realm of\b", "AI tell: 'in the realm of' — just say the domain"),
    (r"\bpaves the way for\b", "cliché: 'paves the way for' — be specific"),
    (r"\bstands as a\b", "AI tell: 'stands as a' — what is it?"),
    (r"\bexists as a\b", "AI tell: 'exists as a'"),
    (r"\bacts as a\b", "AI tell: 'acts as a' — what does it actually do?"),
    (r"\bdynamic\b", "AI tell: 'dynamic' overused for places/economies"),
    (r"\bvibrant\b", "AI tell: 'vibrant' is AI place description"),
    (r"\bbustling\b", "AI tell: 'bustling' is AI prose"),
    (r"\bpicturesque\b", "AI tell: 'picturesque' is AI travel writing"),
    (r"\bbreathtaking\b", "AI tell: 'breathtaking' is thesaurus AI"),
    (r"\bcaptivates\b", "AI tell: 'captivates' is AI prose"),
    (r"\bleverages cutting-edge\b", "AI tell: 'cutting-edge' is marketing AI"),
    (r"\bstate-of-the-art\b", "AI tell: 'state-of-the-art' is marketing speak"),
    (r"\binnovative\b", "AI tell: 'innovative' is unsubstantiated claim"),
    (r"\bpioneering\b", "AI tell: 'pioneering' — can you prove this?"),
    (r"\bgame-changer\b", "AI tell: 'game-changer' — be specific"),
    (r"\b groundbreaking \b", "AI tell: 'groundbreaking'"),
    (r"\bfostering\b", "AI tell: 'fostering' — use 'building' or 'encouraging'"),
    (r"\bgiven the fact that\b", "AI tell: 'given the fact that' → 'because'"),
    (r"\bdue to the fact that\b", "AI tell: 'due to the fact that' → 'because'"),
    (r"\bin light of the fact that\b", "AI tell: 'in light of the fact that' → 'because'"),
]

# Formulaic transitions — AI always signals structure
FORMULAIC = [
    (r"^\s*First[,\s]", "formulaic: 'First,' opener — use something fresher"),
    (r"^\s*Second[,\s]", "formulaic: 'Second,' opener"),
    (r"^\s*Third[,\s]", "formulaic: 'Third,' opener"),
    (r"^\s*Finally[,\s]", "formulaic: 'Finally,' opener"),
    (r"\bIn conclusion\b", "formulaic: 'In conclusion' — just end"),
    (r"\bTo summarize\b", "formulaic: 'To summarize' — just summarize"),
    (r"\bIn summary\b", "formulaic: 'In summary'"),
    (r"\bIt is worth noting that\b", "AI tell: 'It is worth noting that' — just say it"),
    (r"\bIt is important to note that\b", "AI tell: 'It is important to note that' — just say it"),
    (r"\bIt should be noted that\b", "AI tell: 'It should be noted that'"),
    (r"\bAdditionally,\b", "overused transition: 'Additionally,' — vary sentence openers"),
    (r"\bFurthermore,\b", "overused: 'Furthermore,'"),
    (r"\bMoreover,\b", "overused: 'Moreover,'"),
    (r"\bThis (technique|method|approach|framework)\b", "formulaic: 'This technique' at paragraph start"),
    (r"\bThis (article|post|section)\b", "formulaic: 'This article' at start"),
    (r"\bWith that said\b", "formulaic transition"),
    (r"\bThat being said\b", "formulaic transition"),
    (r"\bHaving said that\b", "formulaic transition"),
]

# Hedging without value
HEDGING = [
    (r"\bit is possible that\b", "hedging: 'it is possible that' — how likely?"),
    (r"\bmay potentially\b", "hedging: double modal"),
    (r"\bmight potentially\b", "hedging: double modal"),
    (r"\bappears to be\b", "hedging: 'appears to be' — what is it?"),
    (r"\bseems to\b", "hedging: 'seems to' — what does the evidence show?"),
    (r"\bsuggests that\b", "hedging: 'suggests that' — what is the evidence?"),
    (r"\bwould seem to\b", "hedging: 'would seem to'"),
    (r"\bcan be seen as\b", "hedging: 'can be seen as' — say what it is"),
    (r"\bmay be considered\b", "hedging: 'may be considered'"),
    (r"\ba range of\b", "hedging: 'a range of' — what range specifically?"),
    (r"\bto some extent\b", "hedging: 'to some extent' — how much?"),
    (r"\bin some cases\b", "hedging: 'in some cases' — which cases?"),
    (r"\bnotably\b", "overuse: 'notably' signals AI emphasis"),
    (r"\bparticularly\b", "overuse: 'particularly' signals AI emphasis"),
    (r"\bespecially\b", "overuse: 'especially' signals AI emphasis"),
]

# Passive voice — AI hides who does what
PASSIVE = [
    (r"\bit was determined that\b", "passive: 'it was determined that'"),
    (r"\bit has been shown that\b", "passive: 'it has been shown that'"),
    (r"\bit can be seen that\b", "passive: 'it can be seen that'"),
    (r"\bis being used to\b", "passive: 'is being used to'"),
    (r"\bwas developed by\b", "passive: 'was developed by' — who?"),
    (r"\bhas been developed\b", "passive: 'has been developed' — by whom?"),
    (r"\bwas created by\b", "passive: 'was created by' — who?"),
    (r"\bhas been implemented\b", "passive: 'has been implemented' — by whom?"),
]

ALL_PATTERNS = [
    ("VAGUE FILLER", VAGUE_FILLER),
    ("FORMULAIC TRANSITION", FORMULAIC),
    ("HEDGING", HEDGING),
    ("PASSIVE VOICE", PASSIVE),
]


def check_file(filepath: str) -> list[tuple[str, str, str, int]]:
    """Check a file for AI tells. Returns list of (category, pattern, line, line_num)."""
    if not os.path.exists(filepath):
        return []

    if filepath.endswith(".md"):
        # Also check .astro files (Astro markdown components)
        pass

    issues = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            # Skip code blocks
            if "```" in line:
                continue
            for category, pattern_list in ALL_PATTERNS:
                for pattern, description in pattern_list:
                    m = re.search(pattern, line, re.IGNORECASE)
                    if m:
                        issues.append((category, description, line.strip(), line_num))
                        break  # one issue per category per line
    return issues


def main():
    if len(sys.argv) < 2:
        print("Usage: check-blog-ai-tells.py <file1> [file2 ...]")
        sys.exit(2)

    # Get staged files from git if no args (hook mode)
    files = sys.argv[1:]

    all_issues = []
    for filepath in files:
        # Only check markdown and astro content files
        if not (filepath.endswith(".md") or filepath.endswith(".astro")):
            continue
        issues = check_file(filepath)
        if issues:
            all_issues.append((filepath, issues))

    if not all_issues:
        print("✓ No AI tells detected — clean")
        sys.exit(0)

    # Print report
    print("\n" + "=" * 60)
    print("BLOG EDITOR: AI tells detected — commit blocked")
    print("=" * 60)

    for filepath, issues in all_issues:
        print(f"\n{filepath}:")
        seen = set()
        for category, description, line, line_num in issues:
            key = (category, line_num)
            if key in seen:
                continue
            seen.add(key)
            print(f"  L{line_num}: [{category}]")
            print(f"    {description}")
            print(f"    In:    {line[:80]}{'...' if len(line) > 80 else ''}")

    print("\n" + "-" * 60)
    print("Fix these before committing. If the pattern is a false positive,")
    print("you can bypass with: git commit --no-verify")
    print("(Use sparingly — the editor will notice.)")
    print("-" * 60)
    sys.exit(1)


if __name__ == "__main__":
    main()
