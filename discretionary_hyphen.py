"""Leave U+00AD line-breaking to applications; supply an actual U+2010 dash.

The old discretionary dash drawing remains a component, with its point/hint
data unchanged. Ordinary hyphen and every existing visible letter are retained.
Default-ignorable-preserving/raw glyph APIs may report .notdef for U+00AD;
application line-breaking behavior must be tested separately.
"""
from fontTools.ttLib.tables._g_l_y_f import Glyph,GlyphComponent

def configure_discretionary_hyphen(font):
    cmap=font.getBestCmap()
    if 0x2010 not in cmap:
        source=cmap.get(0xAD)
        if source is None:raise ValueError('Original discretionary dash drawing missing')
        name='uni2010'
        if name in font.getGlyphOrder():raise ValueError('Unmapped U+2010 glyph exists')
        glyph=Glyph();glyph.numberOfContours=-1
        component=GlyphComponent();component.glyphName=source
        component.x=component.y=0;component.flags=4
        glyph.components=[component]
        order=font.getGlyphOrder()[:]
        font['glyf'][name]=glyph;glyph.recalcBounds(font['glyf'])
        font['hmtx'].metrics[name]=(font['hmtx'].metrics[source][0],glyph.xMin)
        font.setGlyphOrder(order+[name])
        font['GDEF'].table.GlyphClassDef.classDefs[name]=1
    else:name=cmap[0x2010]
    for table in font['cmap'].tables:
        if table.isUnicode():
            table.cmap[0x2010]=name
            table.cmap.pop(0xAD,None)
