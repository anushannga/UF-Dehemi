"""Portable build retaining upstream TrueType layouts and italic artwork."""
from pathlib import Path
from math import tan, radians
from fontTools.ttLib import TTFont, newTable
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.transformPen import TransformPen
ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'fonts/ttf/dehemi'
OUT.mkdir(parents=True, exist_ok=True)
VERSION='2.420'
FAMILY='Dehemi'
PREFIX='Dehemi'
NOTICE='Copyright 2026 The Dehemi Project Authors (https://github.com/anushannga/UF-Dehemi). Copyright 2015-2023 The Maname Project Authors (https://github.com/mooniak/maname-font). Dehemi modifications by Pasan Anushanga. Release prepared for ANUSHANGA K P.'

def add_glyph(font,name,glyph,width,codepoint):
    order=font.getGlyphOrder()[:]
    font['glyf'][name]=glyph
    font['hmtx'].metrics[name]=(width,0)
    font.setGlyphOrder(order+[name])
    glyph.recalcBounds(font['glyf'])
    font['hmtx'].metrics[name]=(width,getattr(glyph,'xMin',0))
    for table in font['cmap'].tables:
        if table.isUnicode():table.cmap[codepoint]=name

def add_chandrabindu(font):
    shear=tan(radians(14))
    pen=TTGlyphPen(None);p=TransformPen(pen,(1,0,shear,1,0,0))
    # A crescent containing a dot, positioned above a base per Unicode reference.
    p.moveTo((-140,840));p.qCurveTo((-120,700),(0,700))
    p.qCurveTo((120,700),(140,840));p.lineTo((95,840))
    p.qCurveTo((80,745),(0,745));p.qCurveTo((-80,745),(-95,840));p.closePath()
    p.moveTo((0,835));p.qCurveTo((30,835),(30,805));p.qCurveTo((30,775),(0,775))
    p.qCurveTo((-30,775),(-30,805));p.qCurveTo((-30,835),(0,835));p.closePath()
    add_glyph(font,'sinChandrabindu',pen.glyph(),0,0xD81)
    attach_chandrabindu(font)

def attach_chandrabindu(font,base_font=None):
    from fontTools.otlLib.builder import buildAnchor,buildLookup,buildMarkBasePosSubtable
    base_font=base_font or font
    shear=tan(radians(14))
    classes=font['GDEF'].table.GlyphClassDef.classDefs
    classes['sinChandrabindu']=3
    marks={'sinChandrabindu':(0,buildAnchor(round(shear*700),700))}
    bases={}
    dotted_circle=font.getBestCmap().get(0x25CC)
    for name in base_font.getGlyphOrder():
        glyph=base_font['glyf'][name]
        if (name.startswith('sin') or name==dotted_circle) and classes.get(name)!=3 and base_font['hmtx'].metrics[name][0]>0 and hasattr(glyph,'yMax'):
            bases[name]={0:buildAnchor(round((glyph.xMin+glyph.xMax)/2),glyph.yMax+35)}
    lookup=buildLookup([buildMarkBasePosSubtable(marks,bases,font.getReverseGlyphMap())])
    table=font['GPOS'].table;index=len(table.LookupList.Lookup)
    table.LookupList.Lookup.append(lookup);table.LookupList.LookupCount=len(table.LookupList.Lookup)
    for record in table.FeatureList.FeatureRecord:
        if record.FeatureTag=='abvm':
            record.Feature.LookupListIndex.append(index)
            record.Feature.LookupCount=len(record.Feature.LookupListIndex)

def add_rupee(font):
    pen=TTGlyphPen(None);p=TransformPen(pen,(1,0,tan(radians(14)),1,0,0))
    for points in [[(35,620),(515,620),(515,575),(35,575)],[(35,500),(515,500),(515,455),(35,455)]]:
        p.moveTo(points[0])
        for point in points[1:]:p.lineTo(point)
        p.closePath()
    p.moveTo((130,575));p.lineTo((260,575));p.qCurveTo((450,575),(450,430))
    p.qCurveTo((450,305),(280,300));p.lineTo((500,0));p.lineTo((395,0))
    p.lineTo((155,320));p.lineTo((155,360));p.lineTo((245,360))
    p.qCurveTo((365,360),(365,430));p.qCurveTo((365,530),(260,530));p.lineTo((130,530));p.closePath()
    add_glyph(font,'uni20B9',pen.glyph(),550,0x20B9)

def build(style):
    f = TTFont(recalcTimestamp=False)
    f.importXML(ROOT / 'sources/Upstream-Tight232.ttx')
    from native_features import compile_features,unskew_positioning
    compile_features(f)
    f['hmtx'].metrics['uni02C9'] = (550,178)
    add_chandrabindu(f)
    add_rupee(f)
    for cp in [0x2028,0x2029]:add_glyph(f,f'uni{cp:04X}',TTGlyphPen(None).glyph(),0,cp)
    for name in ['multiply','less','greater','equal','divide','plus','minus']:
        _,lsb=f['hmtx'].metrics[name];f['hmtx'].metrics[name]=(550,lsb)
    if style == 'Regular':
        glyphset=f.getGlyphSet()
        fresh={}
        shear=tan(radians(-14))
        unskew_positioning(f,shear)
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
    configure_metadata(f,style)
    f.save(OUT / f'{PREFIX}-{style}.ttf')

def configure_metadata(f,style):
    f['head'].fontRevision=float(VERSION)
    f['OS/2'].fsType=0
    f['OS/2'].fsSelection |= 0x100
    f['OS/2'].recalcAvgCharWidth(f)
    f['hhea'].caretSlopeRise=1000
    f['hhea'].caretSlopeRun=249 if style=='Italic' else 0
    names={0:NOTICE,1:FAMILY,2:style,3:f'{VERSION};UFDE;{PREFIX}-{style}',4:f'{FAMILY} {style}',5:f'Version {VERSION}',6:f'{PREFIX}-{style}'}
    for nid in [16,17]: f['name'].removeNames(nameID=nid)
    for nid,value in names.items():
        f['name'].removeNames(nameID=nid)
        for plat,enc,lang in [(3,1,0x409),(1,0,0)]:f['name'].setName(value,nid,plat,enc,lang)
    f['meta']=newTable('meta');f['meta'].data={'dlng':'Sinh, Latn','slng':'Sinh, Latn'}
    from fontTools.otlLib.builder import buildStatTable
    value={'value':0 if style=='Regular' else 1,'name':'Roman' if style=='Regular' else 'Italic','flags':2 if style=='Regular' else 0}
    if style=='Regular':value['linkedValue']=1
    buildStatTable(f,[{'tag':'ital','name':'Italic','ordering':0,'values':[value]}])

if __name__=='__main__':
    for style in ['Regular','Italic']:build(style)
