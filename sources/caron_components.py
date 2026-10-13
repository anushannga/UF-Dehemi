"""Maintain distinctive caron accents as independently editable components.

The four original alternate carons contain their own short accent drawings.
Split each body and final accent contour without substituting punctuation or
the triangular combining caron. Absolute coordinates and component order keep
the original expanded point indices and parent TrueType program unchanged.
"""
from array import array
from copy import deepcopy
from fontTools.ttLib.tables._g_l_y_f import Glyph, GlyphComponent, GlyphCoordinates
from fontTools.ttLib.tables.ttProgram import Program

CARON_GLYPHS=('Lcaron','dcaron','lcaron','tcaron')

def componentize_alt_carons(font):
    glyphs=font['glyf'];order=font.getGlyphOrder()[:]
    report={}
    for name in CARON_GLYPHS:
        original=glyphs[name]
        partnames=[name+'.body',name+'.caron']
        if original.isComposite() and [c.glyphName for c in original.components]==partnames:
            report[name]={'already_composed':True}
            continue
        if original.numberOfContours<2:
            raise ValueError(f'Expected separate body/accent contours: {name}')
        split=original.endPtsOfContours[-2]+1
        parts=[('body',0,split,list(original.endPtsOfContours[:-1])),
               ('caron',split,len(original.coordinates),[len(original.coordinates)-split-1])]
        components=[]
        for suffix,lo,hi,ends in parts:
            partname=name+'.'+suffix
            part=Glyph();part.numberOfContours=len(ends)
            part.coordinates=GlyphCoordinates(original.coordinates[lo:hi])
            part.flags=array('B',original.flags[lo:hi]);part.endPtsOfContours=ends
            part.program=Program();part.program.fromBytecode(b'')
            glyphs[partname]=part;part.recalcBounds(glyphs)
            width=font['hmtx'].metrics[name][0] if suffix=='body' else 0
            font['hmtx'].metrics[partname]=(width,part.xMin)
            if partname not in order:order.append(partname)
            component=GlyphComponent();component.glyphName=partname
            component.x=component.y=0;component.flags=4
            components.append(component)
            font['GDEF'].table.GlyphClassDef.classDefs[partname]=1 if suffix=='body' else 3
        body,accent=(glyphs[n] for n in partnames)
        if not accent.yMax>body.yMax:
            raise ValueError(f'Last contour was not an upper caron accent: {name}')
        compound=Glyph();compound.numberOfContours=-1;compound.components=components
        if hasattr(original,'program'):compound.program=deepcopy(original.program)
        glyphs[name]=compound;compound.recalcBounds(glyphs)
        if original.getCoordinates(glyphs)!=compound.getCoordinates(glyphs):
            raise ValueError(f'Expanded point order changed: {name}')
        if hasattr(original,'program') and original.program.getBytecode()!=compound.program.getBytecode():
            raise ValueError(f'Parent hint instructions changed: {name}')
        report[name]={'components':partnames,'point_order_preserved':True,'parent_instructions_preserved':True}
    font.setGlyphOrder(order)
    return report
