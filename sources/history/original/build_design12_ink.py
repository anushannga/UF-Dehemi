#!/usr/bin/env python3
"""Add an original dry-ink texture to the UF-Dehemi Design 12 outlines.

The texture evokes the supplied reference's broken-ink behaviour without
copying any of its glyph outlines. Cuts are deterministic per glyph so every
build is reproducible and contextual forms keep a coherent texture density.
"""
from __future__ import annotations

import hashlib
import json
import random
from pathlib import Path

import pathops
import uharfbuzz as hb
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.cu2quPen import Cu2QuPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "UF-Dehemi-Design12" / "UF-Dehemi.ttf"
OUTDIR = ROOT / "UF-Dehemi-Design12-Ink"
OUTPUT = OUTDIR / "UF-Dehemi-Ink.ttf"


def set_name(font, name_id, value):
    table = font["name"]
    table.removeNames(nameID=name_id)
    table.setName(value, name_id, 3, 1, 0x409)
    table.setName(value, name_id, 1, 0, 0)


def bounds(path):
    pen = BoundsPen(None)
    path.draw(pen)
    return pen.bounds or (0, 0, 0, 0)


def rect_path(x0, y0, x1, y1, skew=0):
    p = pathops.Path()
    p.moveTo(x0, y0)
    p.lineTo(x1, y0 + skew)
    p.lineTo(x1, y1 + skew)
    p.lineTo(x0, y1)
    p.close()
    return p


def to_glyph(path):
    path = pathops.simplify(path)
    path.convertConicsToQuads(0.25)
    pen = TTGlyphPen(None)
    path.draw(Cu2QuPen(pen, max_err=0.7, reverse_direction=False))
    return pen.glyph()


def glyph_path(glyph_set, name):
    p = pathops.Path()
    glyph_set[name].draw(p.getPen(glyphSet=glyph_set))
    return pathops.simplify(p) if p else p


def distress(path, name, width):
    x0, y0, x1, y1 = bounds(path)
    w, h = x1 - x0, y1 - y0
    if w < 150 or h < 180 or width == 0:
        return path, 0

    rng = random.Random("UF-Dehemi-Ink-2.200/" + name)
    # A consistent dry-brush band crosses the lower-middle ink mass. Vary its
    # height slightly per glyph so text does not look mechanically stamped.
    band = y0 + h * rng.uniform(0.34, 0.46)
    count = 2 if w < 420 else 3 if w < 760 else 4
    cuts = pathops.Path()
    for i in range(count):
        seg_w = w * rng.uniform(0.12, 0.31)
        start = x0 + w * rng.uniform(0.03, 0.88) - seg_w * 0.35
        start = max(x0 - 4, min(start, x1 - seg_w))
        thickness = rng.uniform(4.0, 9.0)
        y = band + rng.uniform(-15, 15)
        cut = rect_path(start, y, start + seg_w, y + thickness, rng.uniform(-3, 3))
        cuts = cut if not cuts else pathops.op(cuts, cut, pathops.PathOp.UNION)

    # A second, much sparser hairline gives the natural split-ink appearance
    # seen in broad nib work without turning counters into noise.
    if h > 430 and rng.random() < 0.72:
        y = band + rng.uniform(18, 35)
        cut = rect_path(x0 + w * .18, y, x0 + w * rng.uniform(.52, .82), y + rng.uniform(2, 5), 1)
        cuts = pathops.op(cuts, cut, pathops.PathOp.UNION)

    try:
        return pathops.simplify(pathops.op(path, cuts, pathops.PathOp.DIFFERENCE)), count
    except Exception:
        return path, 0


def shape(font_path, text):
    font = hb.Font(hb.Face(font_path.read_bytes()))
    buf = hb.Buffer(); buf.add_str(text); buf.guess_segment_properties(); hb.shape(font, buf)
    ids = [i.codepoint for i in buf.glyph_infos]
    return {"text": text, "glyph_count": len(ids), "missing_glyphs": ids.count(0)}


def main():
    OUTDIR.mkdir(exist_ok=True)
    font = TTFont(SOURCE, recalcBBoxes=True, recalcTimestamp=False)
    source = TTFont(SOURCE)
    gs = source.getGlyphSet()
    glyf = font["glyf"]
    hmtx = font["hmtx"].metrics
    textured = 0
    total_cuts = 0

    for name in font.getGlyphOrder():
        p = glyph_path(gs, name)
        if not p:
            continue
        p, cuts = distress(p, name, hmtx[name][0])
        if cuts:
            glyf[name] = to_glyph(p)
            textured += 1
            total_cuts += cuts

    # Outline edits invalidate the previous hint programs.
    for tag in ("fpgm", "prep", "cvt ", "LTSH", "hdmx", "VDMX"):
        if tag in font:
            del font[tag]
    for glyph in glyf.glyphs.values():
        if hasattr(glyph, "program"):
            try: glyph.removeHinting()
            except Exception: pass

    names = {
        1: "UF-Dehemi Ink",
        2: "Regular",
        3: "2.200;UFDE;UF-Dehemi-Ink",
        4: "UF-Dehemi Ink Regular",
        5: "Version 2.200; Design 12 dry-ink texture",
        6: "UF-Dehemi-Ink",
        10: "UF-Dehemi Design 12 with original deterministic dry-brush ink cuts.",
        16: "UF-Dehemi Ink",
        17: "Regular",
    }
    for name_id, value in names.items():
        set_name(font, name_id, value)
    font["head"].fontRevision = 2.2
    font["head"].modified = 3852316800
    font.save(OUTPUT, reorderTables=True)

    samples = [
        "සිංහල අකුරු ලස්සනට ලියමු",
        "ශ්‍රී ලංකාවේ ක්‍රියාකාරී භාෂාව",
        "කා කි කී කු කූ කෘ කෙ කේ කෛ කො කෝ කෞ ක් ක්‍ර ක්‍ය",
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ abcdefghijklmnopqrstuvwxyz 0123456789",
    ]
    report = {
        "font": OUTPUT.name,
        "version": "2.200",
        "texture": "original deterministic dry-brush cuts",
        "textured_glyphs": textured,
        "primary_cuts": total_cuts,
        "total_glyphs": len(font.getGlyphOrder()),
        "shaping_tests": [shape(OUTPUT, s) for s in samples],
        "sha256_before_autohint": hashlib.sha256(OUTPUT.read_bytes()).hexdigest(),
    }
    (OUTDIR / "validation-report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
