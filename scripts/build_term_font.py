#!/usr/bin/env python3
"""Cut the terminal-capture font: one subset of DejaVu Sans Mono for every cell of a frame.

Authoring-time only, like build_pages.py: it needs fontTools and brotli and the DejaVu
files on this machine, and writes assets/term-Regular.woff2, assets/term-Bold.woff2 and
assets/term-LICENSE.txt. Nothing here runs at publish time. A captured frame must take
every cell from one font, or symbols fall back to a font with another advance width and
the columns drift. The character list is term_glyphs.RANGES; build_pages.py refuses a
frame that uses a character outside it.
"""
import sys
from pathlib import Path
from fontTools import subset
from fontTools.ttLib import TTFont
sys.path.insert(0, str(Path(__file__).parent))
from term_glyphs import RANGES

SITE = Path(__file__).resolve().parent.parent
SOURCE = Path("/usr/share/fonts/truetype/dejavu")
FAMILY = "Writfold Term"
def cut(source, style, target):
    font = TTFont(source, recalcTimestamp=False)  # the same bytes on every run
    licence = font["name"].getDebugName(13)
    options = subset.Options(flavor="woff2", layout_features=[], hinting=False, desubroutinize=True,
                             name_IDs=[0, 1, 2, 3, 4, 5, 6], notdef_outline=True)
    cutter = subset.Subsetter(options)
    cutter.populate(unicodes=[c for lo, hi in RANGES for c in range(lo, hi + 1)])
    cutter.subset(font)
    missing = [f"U+{c:04X}" for lo, hi in RANGES for c in range(lo, hi + 1) if c not in font.getBestCmap()]
    if missing:
        raise SystemExit(f"{source.name} lacks {' '.join(missing)}")
    # A modified copy must not keep the original names; the copyright record (ID 0) stays.
    for record in font["name"].names:
        text = {1: FAMILY, 2: style, 3: f"{FAMILY} {style}; subset of {source.stem} {font['name'].getDebugName(5)}",
                4: f"{FAMILY} {style}", 6: f"{FAMILY.replace(' ', '')}-{style}"}.get(record.nameID)
        if text:
            record.string = text
    font.flavor = "woff2"
    font.save(target)
    return licence

def main():
    licence = cut(SOURCE / "DejaVuSansMono.ttf", "Regular", SITE / "assets/term-Regular.woff2")
    cut(SOURCE / "DejaVuSansMono-Bold.ttf", "Bold", SITE / "assets/term-Bold.woff2")
    (SITE / "assets/term-LICENSE.txt").write_text(
        f"{FAMILY} (assets/term-Regular.woff2, assets/term-Bold.woff2) is a subset of DejaVu Sans Mono,\n"
        "renamed as its licence requires of a modified copy. The licence carried in the font follows.\n\n"
        + licence.replace("\r\n", "\n").rstrip() + "\n", encoding="utf-8")
    print("cut", FAMILY)

if __name__ == "__main__":
    sys.exit(main())
