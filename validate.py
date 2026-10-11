from pathlib import Path
import json, hashlib
from fontTools.ttLib import TTFont
import uharfbuzz as hb
import freetype
from build import VERSION,FAMILY,PREFIX,OUT,NOTICE
R=Path(__file__).resolve().parent
paths={s:OUT/f'{PREFIX}-{s}.ttf' for s in ['Regular','Italic']}
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
    cmap=font.getBestCmap()
    missing=[cp for cp in range(0xd80,0xe00) if __import__('unicodedata').name(chr(cp),'') and cp not in cmap]
    assert not missing,(style,missing)
    assert font['name'].getDebugName(1)==FAMILY
    assert font['name'].getDebugName(0)==NOTICE==(R/'OFL.txt').read_text(encoding='utf8').splitlines()[0]
    assert font['name'].getDebugName(2)==style
    assert not any(n.nameID in [16,17] for n in font['name'].names)
    assert font['hmtx'].metrics[cmap[0x2C9]][0]>0
    assert font['hmtx'].metrics[cmap[0xD81]][0]==0
    assert font['GDEF'].table.GlyphClassDef.classDefs[cmap[0xD81]]==3
    assert font['OS/2'].fsType==0 and font['OS/2'].fsSelection&0x100
    for cp in [0x2028,0x2029]:
        assert cp in cmap and font['hmtx'].metrics[cmap[cp]][0]==0 and font['glyf'][cmap[cp]].numberOfContours==0
    assert 0x20B9 in cmap
    assert 'STAT' in font and font['meta'].data['dlng']=='Sinh, Latn'
    for text in samples:assert all(g[0] for g in shape(data,text)),(style,text)
    face=freetype.Face(str(path))
    for size in [12,16,24,48,96]:
        face.set_pixel_sizes(0,size)
        for gid in range(len(font.getGlyphOrder())):face.load_glyph(gid,freetype.FT_LOAD_RENDER)
    if style=='Italic':
        for name in old.getGlyphOrder():
            assert old['glyf'][name].getCoordinates(old['glyf'])==font['glyf'][name].getCoordinates(font['glyf']),name
            assert getattr(old['glyf'][name],'program',None).getBytecode()==getattr(font['glyf'][name],'program',None).getBytecode() if hasattr(old['glyf'][name],'program') else not hasattr(font['glyf'][name],'program'),name
        for text in samples:
            if '\u0d81' not in text:assert shape(reference,text)==shape(data,text),text
    markid=font.getGlyphID('sinChandrabindu')
    positioned=shape(data,'ක\u0d81')
    assert any(g[0]==markid and g[1]==0 and g[4]!=0 for g in positioned),(style,positioned)
    result[style]={'shaping_cases':len(samples),'rendered_glyphs':len(font.getGlyphOrder())*5,'sha256':hashlib.sha256(data).hexdigest(),'sinhala_assigned_coverage':True,'metadata_coverage_mark_attachment_assertions':True}
(R/'qa'/f'validation-{VERSION}.json').write_text(json.dumps(result,indent=2),encoding='utf8')
print(json.dumps(result))
