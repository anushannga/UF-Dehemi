"""Portable build retaining upstream TrueType layouts and italic artwork."""
from pathlib import Path
from math import tan, radians
import copy
from fontTools.ttLib import TTFont
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.transformPen import TransformPen
ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'fonts/ttf/ufdehemi'
OUT.mkdir(parents=True, exist_ok=True)

def build(style):
    f = TTFont(recalcTimestamp=False)
    f.importXML(ROOT / 'sources/Upstream-Tight232.ttx')
    f['hmtx'].metrics['uni02C9'] = (550,178)
    # Chandrabindu: source anusvara ring with a smaller dot above it.
    from fontTools.pens.recordingPen import DecomposingRecordingPen
    glyphset=f.getGlyphSet()
    p = TTGlyphPen(None)
    for name,transform in [('sinAnusvara',(1,0,0,1,0,0)),('period',(.65,0,0,.65,210,480))]:
        rec=DecomposingRecordingPen(glyphset)
        glyphset[name].draw(rec)
        rec.replay(TransformPen(p,transform))
    order=f.getGlyphOrder()[:]
    f['glyf']['sinChandrabindu'] = p.glyph()
    f['hmtx'].metrics['sinChandrabindu'] = (398,107)
    f.setGlyphOrder(order+['sinChandrabindu'])
    for table in f['cmap'].tables:
        if table.isUnicode(): table.cmap[0xD81]='sinChandrabindu'
    if style == 'Regular':
        glyphset=f.getGlyphSet()
        fresh={}
        shear=tan(radians(-14))
        for name in f.getGlyphOrder():
            pen=TTGlyphPen(None)
            from fontTools.pens.recordingPen import DecomposingRecordingPen
            rec=DecomposingRecordingPen(glyphset)
            glyphset[name].draw(rec)
            rec.replay(TransformPen(pen,(1,0,shear,1,0,0)))
            fresh[name]=pen.glyph()
        for name,glyph in fresh.items():
            f['glyf'][name]=glyph
            glyph.recalcBounds(f['glyf'])
            advance,_=f['hmtx'].metrics[name]
            f['hmtx'].metrics[name]=(advance,getattr(glyph,'xMin',0))
        for tag in ['fpgm','prep','cvt ','VDMX','LTSH','hdmx']:
            if tag in f: del f[tag]
        f['post'].italicAngle=0
        f['OS/2'].fsSelection=(f['OS/2'].fsSelection & ~1)|64
        f['head'].macStyle &= ~2
    f['head'].fontRevision=2.4
    f['OS/2'].fsType=0
    f['hhea'].caretSlopeRise=1000
    f['hhea'].caretSlopeRun=249 if style=='Italic' else 0
    names={1:'UF Dehemi',2:style,3:f'2.400;UFDE;UFDehemi-{style}',4:f'UF Dehemi {style}',5:'Version 2.400',6:f'UFDehemi-{style}'}
    for nid in [16,17]: f['name'].removeNames(nameID=nid)
    for nid,value in names.items():
        f['name'].removeNames(nameID=nid)
        for plat,enc,lang in [(3,1,0x409),(1,0,0)]:f['name'].setName(value,nid,plat,enc,lang)
    f.save(OUT / f'UFDehemi-{style}.ttf')

if __name__=='__main__':
    for style in ['Regular','Italic']:build(style)
