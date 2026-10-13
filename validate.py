from pathlib import Path
import json, hashlib
from fontTools.ttLib import TTFont
import uharfbuzz as hb
import freetype
from build import VERSION,FAMILY,PREFIX,OUT,NOTICE,LICENSE_DESCRIPTION,LICENSE_URL
from sources.latin_extensions import AUXILIARY_CODEPOINTS,CARON_BASES
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
    assert (OUT/'OFL.txt').read_bytes()==(R/'OFL.txt').read_bytes()
    for nid,expected in [(13,LICENSE_DESCRIPTION),(14,LICENSE_URL)]:
        records=[n for n in font['name'].names if n.nameID==nid]
        assert records and all(n.toUnicode()==expected for n in records),(style,nid)
    assert not any(n.nameID in [16,17] for n in font['name'].names)
    assert font['hmtx'].metrics[cmap[0x2C9]][0]>0
    assert font['hmtx'].metrics[cmap[0xD81]][0]==0
    assert font['GDEF'].table.GlyphClassDef.classDefs[cmap[0xD81]]==3
    assert font['OS/2'].fsType==0 and font['OS/2'].fsSelection&0x100
    assert font['hmtx'].metrics['sinVirama'][0]==0
    assert (font['hhea'].ascent,font['hhea'].descent)==(1167,-333)
    assert (font['OS/2'].sTypoAscender,font['OS/2'].sTypoDescender)==(1167,-333)
    assert font['head'].yMax<=font['hhea'].ascent and font['head'].yMin>=font['hhea'].descent
    assert all(cp in cmap for cp in AUXILIARY_CODEPOINTS)
    assert 0xAD not in cmap and 0x2010 in cmap
    assert font['hmtx'].metrics[cmap[0x2010]][0]==font['hmtx'].metrics[cmap[0x2D]][0]
    shy=shape(data,'co\u00adoperate');plain=shape(data,'cooperate')
    assert all(g[0] for g in shy) and sum(g[1] for g in shy)==sum(g[1] for g in plain)
    assert [g[0] for g in shy if g[1]]==[g[0] for g in plain if g[1]]
    from sources.caron_components import CARON_GLYPHS
    for name in CARON_GLYPHS:
        assert font['glyf'][name].isComposite(),(style,name)
        assert [c.glyphName for c in font['glyf'][name].components]==[name+'.body',name+'.caron']
        assert font['hmtx'].metrics[name+'.caron'][0]==0
    for cp in [0x2028,0x2029]:
        assert cp in cmap and font['hmtx'].metrics[cmap[cp]][0]==0 and font['glyf'][cmap[cp]].numberOfContours==0
    assert 0x20B9 in cmap
    assert 'STAT' in font and font['meta'].data['dlng']=='Sinh, Latn'
    for text in samples:assert all(g[0] for g in shape(data,text)),(style,text)
    for cp in CARON_BASES:
        nfc=chr(cp);nfd=__import__('unicodedata').normalize('NFD',nfc)
        assert shape(data,nfc)==shape(data,nfd),(style,hex(cp))
    assert any(g[3] or g[4] for g in shape(data,'l\u0303')[1:]),(style,'l+tilde attachment')
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
    viramaid=font.getGlyphID('sinVirama');positioned=shape(data,'◌්')
    assert any(g[0]==viramaid and g[1]==0 and (g[3] or g[4]) for g in positioned),(style,positioned)
    result[style]={'shaping_cases':len(samples),'rendered_glyphs':len(font.getGlyphOrder())*5,'sha256':hashlib.sha256(data).hexdigest(),'sinhala_assigned_coverage':True,'metadata_coverage_mark_attachment_assertions':True,'license_metadata_and_bundled_license':True,'auxiliary_latin_codepoints':len(AUXILIARY_CODEPOINTS),'nfc_nfd_comparisons':len(CARON_BASES),'virama_dotted_circle_attachment':True,'line_height_units':1500,'previous_line_height_units':1553}
(R/'qa'/f'validation-{VERSION}.json').write_text(json.dumps(result,indent=2),encoding='utf8')
print(json.dumps(result))
