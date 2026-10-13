#!/usr/bin/env python3
"""Build UF-Dehemi from the approved Design 12 drawing system.

Unlike the earlier prototype, this applies one pen transform to the complete
Maname Sinhala production set and its Latin companion. It does not splice old
and new outlines. The 59 approved alphabet drawings are then installed exactly
from the Design 12 SVG source (including the selected custom exit strokes).
"""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

import pathops
import uharfbuzz as hb
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.cu2quPen import Cu2QuPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.svgLib.path import parse_path
from fontTools.ttLib import TTFont


ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parent
SOURCE = Path(r"C:\Users\MCTech\Downloads\Sinhala-Fonts-main\maname.ttf")
PATHS = ROOT / "design12_glyph_paths.json"
OUTDIR = PROJECT / "UF-Dehemi-Design12"
OUTPUT = OUTDIR / "UF-Dehemi.ttf"

# Exact transform used to create the approved Design 12 alphabet proof.
SX, SHEAR, SY = 0.91, 0.27, 1.04


def set_name(font: TTFont, name_id: int, value: str) -> None:
    table = font["name"]
    table.removeNames(nameID=name_id)
    table.setName(value, name_id, 3, 1, 0x409)
    table.setName(value, name_id, 1, 0, 0)


def path_bounds(path: pathops.Path):
    pen = BoundsPen(None)
    path.draw(pen)
    return pen.bounds or (0, 0, 0, 0)


def to_glyph(path: pathops.Path):
    path = pathops.simplify(path)
    path.convertConicsToQuads(0.25)
    pen = TTGlyphPen(None)
    path.draw(Cu2QuPen(pen, max_err=0.7, reverse_direction=False))
    return pen.glyph()


def transformed_path(glyph_set, glyph_name: str):
    path = pathops.Path()
    glyph_set[glyph_name].draw(
        TransformPen(path.getPen(glyphSet=glyph_set), (SX, 0, SHEAR, SY, 0, 0))
    )
    return pathops.simplify(path) if path else path


def transform_layout_coordinates(font: TTFont) -> None:
    """Transform GPOS anchors and placement values with the outline matrix."""
    seen: set[int] = set()

    def tx(x, y):
        return round(SX * x + SHEAR * y), round(SY * y)

    def walk(obj):
        if obj is None or isinstance(obj, (str, bytes, int, float, bool)):
            return
        oid = id(obj)
        if oid in seen:
            return
        seen.add(oid)
        if isinstance(obj, (list, tuple)):
            for item in obj:
                walk(item)
            return

        cls = obj.__class__.__name__
        if cls == "Anchor" and hasattr(obj, "XCoordinate"):
            obj.XCoordinate, obj.YCoordinate = tx(obj.XCoordinate, obj.YCoordinate)
        elif cls == "ValueRecord":
            xp = getattr(obj, "XPlacement", 0) or 0
            yp = getattr(obj, "YPlacement", 0) or 0
            if hasattr(obj, "XPlacement") or hasattr(obj, "YPlacement"):
                nx, ny = tx(xp, yp)
                if hasattr(obj, "XPlacement"):
                    obj.XPlacement = nx
                if hasattr(obj, "YPlacement"):
                    obj.YPlacement = ny
            if hasattr(obj, "XAdvance"):
                obj.XAdvance = round(SX * (obj.XAdvance or 0))
            if hasattr(obj, "YAdvance"):
                obj.YAdvance = round(SY * (obj.YAdvance or 0))

        for value in getattr(obj, "__dict__", {}).values():
            walk(value)

    if "GPOS" in font:
        walk(font["GPOS"].table)


def shape(font_path: Path, text: str):
    hb_font = hb.Font(hb.Face(font_path.read_bytes()))
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(hb_font, buf)
    return {
        "text": text,
        "glyph_count": len(buf.glyph_infos),
        "missing_glyphs": sum(info.codepoint == 0 for info in buf.glyph_infos),
        "glyph_ids": [info.codepoint for info in buf.glyph_infos],
    }


def main() -> None:
    OUTDIR.mkdir(exist_ok=True)
    font = TTFont(SOURCE, recalcBBoxes=True, recalcTimestamp=False)
    source = TTFont(SOURCE)
    source_gs = source.getGlyphSet()
    cmap = font.getBestCmap()
    glyf = font["glyf"]
    hmtx = font["hmtx"].metrics

    transformed = 0
    for glyph_name in font.getGlyphOrder():
        path = transformed_path(source_gs, glyph_name)
        if not path:
            continue
        glyf[glyph_name] = to_glyph(path)
        x0, _, x1, _ = path_bounds(path)
        old_width, _ = hmtx[glyph_name]
        width = 0 if old_width == 0 else max(round(old_width * SX), round(x1 + 40))
        hmtx[glyph_name] = (width, round(x0))
        transformed += 1

    # Exact approved base drawings. These SVG paths already contain the same
    # transform and the selected custom exit strokes; no inverse shear is used.
    approved = json.loads(PATHS.read_text(encoding="utf-8"))
    replaced = []
    for cp_hex, svg_path in approved.items():
        cp = int(cp_hex, 16)
        glyph_name = cmap[cp]
        path = pathops.Path()
        parse_path(svg_path, path.getPen())
        path = pathops.simplify(path)
        glyf[glyph_name] = to_glyph(path)
        x0, _, x1, _ = path_bounds(path)
        hmtx[glyph_name] = (round(x1 + 55), round(x0))
        replaced.append({"codepoint": f"U+{cp:04X}", "glyph": glyph_name})

    transform_layout_coordinates(font)

    # Rebuilt outlines invalidate source instructions.
    for tag in ("fpgm", "prep", "cvt ", "LTSH", "hdmx", "VDMX"):
        if tag in font:
            del font[tag]
    for glyph in glyf.glyphs.values():
        if hasattr(glyph, "program"):
            try:
                glyph.removeHinting()
            except Exception:
                pass

    names = {
        0: (
            "Copyright 2026 Pasan Anushanga. Based on Maname, copyright "
            "2015-2023 The Maname Project Authors. SIL Open Font License 1.1."
        ),
        1: "UF-Dehemi",
        2: "Regular",
        3: "2.100;UFDE;UF-Dehemi-Regular",
        4: "UF-Dehemi Regular",
        5: "Version 2.100; Design 12 production rebuild",
        6: "UF-Dehemi-Regular",
        8: "Pasan Anushanga",
        9: "Pasan Anushanga; The Maname Project Authors",
        10: "Expressive high-contrast Sinhala and Latin font based on the approved UF-Dehemi Design 12 drawings.",
        11: "https://github.com/mooniak/maname-font",
        13: "This Font Software is licensed under the SIL Open Font License, Version 1.1.",
        14: "https://openfontlicense.org",
        16: "UF-Dehemi",
        17: "Regular",
    }
    for name_id, value in names.items():
        set_name(font, name_id, value)

    font["head"].fontRevision = 2.1
    font["head"].created = 3852316800
    font["head"].modified = 3852316800
    font["OS/2"].fsType = 0
    font["OS/2"].fsSelection |= 1 << 7
    font["post"].italicAngle = -14

    # Calculate final outline extents, then use one clipping-safe metric box.
    temp = OUTDIR / ".metrics.tmp.ttf"
    font.save(temp, reorderTables=True)
    measured = TTFont(temp, recalcBBoxes=True)
    asc = max(measured["head"].yMax + 40, 1050)
    desc = max(-measured["head"].yMin + 40, 350)
    font["hhea"].ascent = asc
    font["hhea"].descent = -desc
    font["hhea"].lineGap = 0
    os2 = font["OS/2"]
    os2.sTypoAscender = asc
    os2.sTypoDescender = -desc
    os2.sTypoLineGap = 0
    os2.usWinAscent = asc
    os2.usWinDescent = desc
    temp.unlink()

    font.save(OUTPUT, reorderTables=True)
    check = TTFont(OUTPUT)
    check_cmap = check.getBestCmap()
    samples = [
        "සිංහල අකුරු ලස්සනට ලියමු",
        "ශ්‍රී ලංකාවේ ක්‍රියාකාරී භාෂාව",
        "කා කි කී කු කූ කෘ කෙ කේ කෛ කො කෝ කෞ ක් ක්‍ර ක්‍ය",
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "abcdefghijklmnopqrstuvwxyz 0123456789 !@#$%^&*()",
    ]
    report = {
        "font": OUTPUT.name,
        "version": "2.100",
        "source": SOURCE.name,
        "source_license": "SIL Open Font License 1.1",
        "design_reference": "20-collection-sinhala-alphabet.svg",
        "glyphs_transformed_with_one_pen_matrix": transformed,
        "approved_svg_base_glyphs": len(replaced),
        "total_glyphs": len(check.getGlyphOrder()),
        "unicode_codepoints": len(check_cmap),
        "basic_latin_complete": all(cp in check_cmap for cp in range(0x20, 0x7F)),
        "sinhala_codepoints": sum(0x0D80 <= cp <= 0x0DFF for cp in check_cmap),
        "tables": {tag: tag in check for tag in ("GSUB", "GPOS", "GDEF", "cmap", "glyf")},
        "metrics": {"ascent": asc, "descent": -desc, "line_gap": 0},
        "shaping_tests": [shape(OUTPUT, sample) for sample in samples],
        "sha256": hashlib.sha256(OUTPUT.read_bytes()).hexdigest(),
        "replaced": replaced,
    }
    (OUTDIR / "validation-report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    shutil.copy2(PROJECT / "OFL.txt", OUTDIR / "OFL.txt")
    shutil.copy2(ROOT / "20-collection-sinhala-alphabet.svg", OUTDIR / "Design-12-reference.svg")
    print(json.dumps({k: v for k, v in report.items() if k not in ("replaced",)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
