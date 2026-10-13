#!/usr/bin/env python3
"""Apply safe production metrics to the final UF-Dehemi Design 12 font."""
from pathlib import Path
import hashlib
import json
import shutil

import uharfbuzz as hb
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "UF-Dehemi-Design12-Ink" / "UF-Dehemi-Ink-Clean.ttf"
OUTPUT = ROOT / "UF-Dehemi-Design12-Ink" / "UF-Dehemi-Final.ttf"
REPORT = ROOT / "UF-Dehemi-Design12-Ink" / "production-standards-report.json"


def set_name(font, name_id, value):
    table = font["name"]
    table.removeNames(nameID=name_id)
    table.setName(value, name_id, 3, 1, 0x409)
    table.setName(value, name_id, 1, 0, 0)


def shape(path, text):
    font = hb.Font(hb.Face(path.read_bytes()))
    buf = hb.Buffer(); buf.add_str(text); buf.guess_segment_properties(); hb.shape(font, buf)
    gids = [g.codepoint for g in buf.glyph_infos]
    return {"text": text, "glyph_count": len(gids), "missing_glyphs": gids.count(0)}


def main():
    font = TTFont(SOURCE, recalcBBoxes=True, recalcTimestamp=False)
    cmap = font.getBestCmap()
    hmtx = font["hmtx"].metrics

    # Readable 280-unit word space at 1000 UPM; NBSP must match exactly.
    for cp in (0x0020, 0x00A0):
        if cp in cmap:
            name = cmap[cp]
            hmtx[name] = (280, hmtx[name][1])

    # Join controls must never advance the cursor.
    for cp in (0x200C, 0x200D):
        if cp in cmap:
            name = cmap[cp]
            hmtx[name] = (0, 0)

    # Preserve the source's tested Sinhala model: above/below marks substituted
    # by GSUB have zero width, while pre-base and post-base presentation forms
    # retain the positive advances required by the Universal Shaping Engine.
    set_name(font, 3, "2.300;UFDE;UF-Dehemi-Regular")
    set_name(font, 5, "Version 2.300; Design 12 ink production metrics")
    font["head"].fontRevision = 2.3
    font["OS/2"].fsSelection |= 1 << 7
    font.save(OUTPUT, reorderTables=True)

    check = TTFont(OUTPUT)
    features = {}
    for table_tag in ("GSUB", "GPOS"):
        table = check[table_tag].table
        features[table_tag] = sorted({r.FeatureTag for r in table.FeatureList.FeatureRecord})
    tests = [
        "සිංහල අකුරු ලස්සනට ලියමු",
        "ශ්‍රී ලංකාවේ ක්‍රියාකාරී භාෂාව",
        "කා කි කී කු කූ කෘ කෙ කේ කෛ කො කෝ කෞ ක් ක්‍ර ක්‍ය",
        "English 0123456789 !@#$%^&*()",
    ]
    os2, hhea, head = check["OS/2"], check["hhea"], check["head"]
    report = {
        "font": OUTPUT.name,
        "version": "2.300",
        "space_width": check["hmtx"].metrics[cmap[0x20]][0],
        "nbsp_matches_space": check["hmtx"].metrics[cmap[0xA0]][0] == check["hmtx"].metrics[cmap[0x20]][0],
        "zwnj_width": check["hmtx"].metrics[cmap[0x200C]][0],
        "zwj_width": check["hmtx"].metrics[cmap[0x200D]][0],
        "vertical_metrics": {
            "hhea": [hhea.ascent, hhea.descent, hhea.lineGap],
            "typo": [os2.sTypoAscender, os2.sTypoDescender, os2.sTypoLineGap],
            "win": [os2.usWinAscent, os2.usWinDescent],
            "glyph_bbox": [head.yMin, head.yMax],
            "use_typo_metrics": bool(os2.fsSelection & (1 << 7)),
        },
        "features": features,
        "shaping_tests": [shape(OUTPUT, text) for text in tests],
        "sha256_before_final_hint": hashlib.sha256(OUTPUT.read_bytes()).hexdigest(),
    }
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    shutil.copy2(ROOT / "OFL.txt", OUTPUT.parent / "OFL.txt")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
