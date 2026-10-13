#!/usr/bin/env python3
"""Remove tiny detached contour fragments from UF-Dehemi Ink."""
from pathlib import Path
import json

from fontTools.pens.recordingPen import DecomposingRecordingPen, RecordingPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parent.parent
FONT_PATH = ROOT / "UF-Dehemi-Design12-Ink" / "UF-Dehemi-Ink.ttf"
REPORT = ROOT / "UF-Dehemi-Design12-Ink" / "fragment-cleanup.json"


def split_contours(commands):
    contours, current = [], []
    for command in commands:
        op, _ = command
        if op == "moveTo" and current:
            contours.append(current)
            current = []
        current.append(command)
        if op in ("closePath", "endPath"):
            contours.append(current)
            current = []
    if current:
        contours.append(current)
    return contours


def contour_size(contour):
    points = []
    for _, args in contour:
        points.extend(p for p in args if isinstance(p, tuple) and len(p) == 2)
    if not points:
        return 0, 0
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    return max(xs) - min(xs), max(ys) - min(ys)


def main():
    font = TTFont(FONT_PATH, recalcBBoxes=True, recalcTimestamp=False)
    source = TTFont(FONT_PATH)
    glyph_set = source.getGlyphSet()
    glyf = font["glyf"]
    cleaned = []
    removed_total = 0

    for name in font.getGlyphOrder():
        recording = DecomposingRecordingPen(glyph_set)
        glyph_set[name].draw(recording)
        contours = split_contours(recording.value)
        if not contours:
            continue
        kept, removed = [], []
        for contour in contours:
            w, h = contour_size(contour)
            # These near-hairline islands are the visible flecks around the
            # letters. Real dots/marks are substantially larger.
            if w <= 24 and h <= 24:
                removed.append((round(w, 2), round(h, 2)))
            else:
                kept.append(contour)
        if not removed:
            continue
        pen = TTGlyphPen(None)
        for contour in kept:
            sub = RecordingPen()
            sub.value = contour
            sub.replay(pen)
        glyf[name] = pen.glyph()
        removed_total += len(removed)
        cleaned.append({"glyph": name, "removed_contours": removed})

    for tag in ("fpgm", "prep", "cvt ", "LTSH", "hdmx", "VDMX"):
        if tag in font:
            del font[tag]
    for glyph in glyf.glyphs.values():
        if hasattr(glyph, "program"):
            try: glyph.removeHinting()
            except Exception: pass

    font["head"].fontRevision = 2.21
    font.save(FONT_PATH, reorderTables=True)
    report = {
        "font": FONT_PATH.name,
        "version": "2.210",
        "glyphs_cleaned": len(cleaned),
        "detached_fragments_removed": removed_total,
        "threshold": "contour width <= 24 and height <= 24 font units",
        "details": cleaned,
    }
    REPORT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if k != "details"}, indent=2))


if __name__ == "__main__":
    main()
