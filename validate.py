from pathlib import Path
import json, hashlib
from fontTools.ttLib import TTFont
import uharfbuzz as hb
import freetype
R=Path(__file__).resolve().parent
paths={s:R/'fonts/ttf/ufdehemi'/f'UFDehemi-{s}.ttf' for s in ['Regular','Italic']}
old=TTFont();old.importXML(R/'sources/Upstream-Tight232.ttx')
samples=['ශ්‍රී ලංකා','ක්‍රියා','ප්‍රශ්න','විද්‍යාව','න්‍යාය','ක්ෂේත්‍ර','ඇ ඈ','අ\u0d81','\u0d81']
samples += [chr(cp)+suffix for cp in range(0xd9a,0xdc7) if cp in old.getBestCmap() for suffix in ['','ා','ැ','ෑ','ි','ී','ු','ූ','ෘ','ෲ','ෙ','ේ','ෛ','ො','ෝ','ෞ','්','්‍ර','්‍ය']]
def shape(data,text):
    font=hb.Font(hb.Face(data));b=hb.Buffer();b.add_str(text);b.guess_segment_properties();b.language='si';hb.shape(font,b)
    return [(g.codepoint,p.x_advance,p.y_advance,p.x_offset,p.y_offset) for g,p in zip(b.glyph_infos,b.glyph_positions)]
import io
buf=io.BytesIO();old.save(buf);reference=buf.getvalue()
result={}
for style,path in paths.items():
    font=TTFont(path,checkChecksums=2);data=path.read_bytes()
    for text in samples:assert all(g[0] for g in shape(data,text)),(style,text)
    face=freetype.Face(str(path))
    for size in [12,16,24,48,96]:
        face.set_pixel_sizes(0,size)
        for gid in range(len(font.getGlyphOrder())):face.load_glyph(gid,freetype.FT_LOAD_RENDER)
    if style=='Italic':
        for name in old.getGlyphOrder():
            assert old['glyf'][name].getCoordinates(old['glyf'])==font['glyf'][name].getCoordinates(font['glyf']),name
        for text in samples:
            if '\u0d81' not in text:assert shape(reference,text)==shape(data,text),text
    result[style]={'shaping_cases':len(samples),'rendered_glyphs':len(font.getGlyphOrder())*5,'sha256':hashlib.sha256(data).hexdigest(),'sinhala_assigned_coverage':all(cp in font.getBestCmap() for cp in range(0xd80,0xe00) if __import__('unicodedata').name(chr(cp),''))}
(R/'qa/validation-2.400.json').write_text(json.dumps(result,indent=2),encoding='utf8')
print(json.dumps(result))
