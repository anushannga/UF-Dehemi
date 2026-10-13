#!/usr/bin/env python3
"""Remove the five experimental hairline exit tails from UF-Dehemi Ink."""
from pathlib import Path
import json

from fontTools.ttLib import TTFont

from build_design12_ink import bounds as path_bounds, distress, to_glyph
from build_design12_production import SOURCE, SX, transformed_path

ROOT = Path(__file__).resolve().parent.parent
SOURCE_FONT = ROOT / "UF-Dehemi-Design12-Ink" / "UF-Dehemi-Ink.ttf"
FONT_PATH = ROOT / "UF-Dehemi-Design12-Ink" / "UF-Dehemi-Ink-Clean.ttf"
REPORT = ROOT / "UF-Dehemi-Design12-Ink" / "hair-tail-cleanup.json"
TARGETS = "කගනලව"


def main():
    font = TTFont(SOURCE_FONT, recalcBBoxes=True, recalcTimestamp=False)
    master = TTFont(SOURCE)
    master_gs = master.getGlyphSet()
    cmap = font.getBestCmap()
    master_cmap = master.getBestCmap()
    glyf = font["glyf"]
    hmtx = font["hmtx"].metrics
    master_hmtx = master["hmtx"].metrics
    changed = []

    for char in TARGETS:
        cp = ord(char)
        name = cmap[cp]
        master_name = master_cmap[cp]
        clean = transformed_path(master_gs, master_name)
        old_master_width = master_hmtx[master_name][0]
        textured, cuts = distress(clean, name, old_master_width)
        glyf[name] = to_glyph(textured)
        x0, _, x1, _ = path_bounds(textured)
        hmtx[name] = (max(round(old_master_width * SX), round(x1 + 40)), round(x0))
        changed.append({"character": char, "codepoint": f"U+{cp:04X}", "glyph": name, "texture_cuts": cuts})

    for tag in ("fpgm", "prep", "cvt ", "LTSH", "hdmx", "VDMX"):
        if tag in font:
            del font[tag]
    for glyph in glyf.glyphs.values():
        if hasattr(glyph, "program"):
            try: glyph.removeHinting()
            except Exception: pass

    font["head"].fontRevision = 2.22
    font.save(FONT_PATH, reorderTables=True)
    report = {
        "font": FONT_PATH.name,
        "version": "2.220",
        "hairline_exit_tails_removed": len(changed),
        "glyphs": changed,
    }
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
