"""Render a reproducible, targeted review of candidate outline warnings."""
import hashlib
import json
from pathlib import Path

import freetype
from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'documentation' / 'review-2.441'
OUT.mkdir(parents=True, exist_ok=True)
report = json.loads((ROOT / 'qa/fontspector-2.441.json').read_text(encoding='utf-8'))
inventory = []
for filename, sections in report['results'].items():
    for checks in sections.values():
        for check in checks:
            for result in check.get('subresults', []):
                if result.get('severity') == 'WARN':
                    problems = [m['GlyphProblem'] for m in result.get('metadata', []) if 'GlyphProblem' in m]
                    inventory.append({'font': filename, 'check': check['check_id'],
                                      'problem_records': len(problems),
                                      'glyphs': sorted({m['glyph_name'] for m in problems}),
                                      'message': result.get('message', '')})

groups = [
    ['sinA', 'sinI', 'sinIi', 'sinKa', 'sinRa', 'sinSa'],
    ['sinTVa', 'sinTTha', 'sinTTh.virama', 'sinTI', 'sinTVI', 'sinAa'],
]
label = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 19)
small = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 16)
hashes = {}
faces = {}
fonts = {}
for style in ('Regular', 'Italic'):
    path = ROOT / 'fonts' / 'ttf' / 'dehemi' / f'Dehemi-{style}.ttf'
    hashes[style] = hashlib.sha256(path.read_bytes()).hexdigest()
    faces[style] = freetype.Face(str(path))
    fonts[style] = TTFont(path)
proofs = []
for page, names in enumerate(groups, 1):
    canvas = Image.new('RGB', (1600, 1430), 'white')
    draw = ImageDraw.Draw(canvas)
    draw.text((24, 16), 'Dehemi 2.441 candidate: targeted outline review', font=label, fill='#172b40')
    draw.text((24, 47), 'Direct glyph proofs at 24 / 48 / 112 px. Each row: Regular, then Italic. Not shaped text.', font=small, fill='#43546a')
    for row, name in enumerate(names):
        top = 90 + row * 220
        draw.text((24, top), name, font=label, fill='#172b40')
        for column, style in enumerate(('Regular', 'Italic')):
            face, font = faces[style], fonts[style]
            draw.text((250 + column * 660, top), style, font=small, fill='#43546a')
            gid = font.getGlyphID(name)
            for j, size in enumerate((24, 48, 112)):
                x, baseline = 255 + column * 660 + j * 205, top + 150
                face.set_pixel_sizes(0, size)
                face.load_glyph(gid, freetype.FT_LOAD_RENDER)
                bmp = face.glyph.bitmap
                if bmp.width and bmp.rows:
                    mask = Image.frombytes('L', (abs(bmp.pitch), bmp.rows), bytes(bmp.buffer)).crop((0, 0, bmp.width, bmp.rows))
                    canvas.paste('#172b40', (x + face.glyph.bitmap_left, baseline - face.glyph.bitmap_top), mask)
                draw.text((x, top + 192), f'{size} px', font=small, fill='#43546a')
        draw.line((24, top + 214, 1570, top + 214), fill='#d9e0e8')
    target = OUT / f'targeted-outlines-{page}.png'
    canvas.save(target)
    proofs.append(str(target.relative_to(ROOT)).replace('\\', '/'))
record = {'version': '2.441', 'font_sha256': hashes, 'warnings': inventory,
          'targeted_glyphs': groups, 'proofs': proofs,
          'scope': '12 selected glyphs at 24/48/112 px, direct FreeType glyph rendering; not all jaggy records or an application/curator certification.'}
(ROOT / 'qa' / 'warning-triage-2.441.json').write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'proofs': proofs, 'warnings': len(inventory), 'font_sha256': hashes}, indent=2))
