"""Readable Sinhala / Many Weatz-inspired vector design, no font output."""
from pathlib import Path
import random, json, shutil
import uharfbuzz as hb
import cairosvg
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen
from svgpathtools import parse_path

ROOT=Path(__file__).resolve().parent
BASE=Path('C:/Users/MCTech/Downloads/Sinhala-Fonts-main/maname.ttf')
REF=Path('C:/Users/MCTech/Downloads/Sinhala-Fonts-main/manyweatz.ttf')
INK='#211c20';PAPER='#fbf7f0';ACCENT='#956247';MUTED='#80766e'
f=TTFont(BASE);gs=f.getGlyphSet();order=f.getGlyphOrder();upm=f['head'].unitsPerEm
hf=hb.Font(hb.Face(BASE.read_bytes()));hf.scale=(upm,upm)
checks=[]
def label(s,x,y,size=18,color=MUTED):
    return f'<text x="{x}" y="{y}" font-family="Segoe UI, sans-serif" font-size="{size}" fill="{color}">{s}</text>'

def lettering(s,x,y,size,width=1500,styled=True):
    b=hb.Buffer();b.add_str(s);b.guess_segment_properties();hb.shape(hf,b)
    missing=sum(i.codepoint==0 for i in b.glyph_infos)
    checks.append({'text':s,'missing_glyphs':missing})
    sx=.91 if styled else 1;sy=1.04 if styled else 1;slant=.27 if styled else 0
    advance=sum(p.x_advance for p in b.glyph_positions)
    scale=min(size/upm,width/(advance*sx+upm*.20))
    cursor=0;pieces=[];specks=[];scratches=[]
    rng=random.Random(s)
    for info,pos in zip(b.glyph_infos,b.glyph_positions):
        name=order[info.codepoint];pen=SVGPathPen(gs)
        gs[name].draw(TransformPen(pen,(sx,0,slant,sy,0,0)))
        dx=(cursor+pos.x_offset)*sx+pos.y_offset*slant;dy=pos.y_offset*sy
        d=pen.getCommands()
        pieces.append(f'<path d="{d}" transform="translate({dx},{dy})"/>')
        # Small pen-lift exits, confined to non-mark base letters. HA is preserved.
        allowed={f.getBestCmap()[ord(c)] for c in 'කගනලව'}
        if styled and name in allowed and pos.x_advance>upm*.3:
            path=parse_path(d)
            pts=[seg.point(j/10) for seg in path for j in range(11)]
            ymin=min(z.imag for z in pts);ymax=max(z.imag for z in pts)
            low=[z for z in pts if z.imag<ymin+(ymax-ymin)*.24]
            z=max(low,key=lambda z:z.real);a=z.real;c=z.imag
            tail=f'M{a-7},{c+8} C{a+33},{c-38} {a+102},{c-51} {a+166},{c+41} C{a+103},{c-31} {a+39},{c-17} {a-7},{c-3} Z'
            pieces.append(f'<path d="{tail}" transform="translate({dx},{dy})"/>')
        if styled and pos.x_advance>upm*.25:
            bp=BoundsPen(gs);gs[name].draw(bp)
            if bp.bounds:
                l,bot,r,top=bp.bounds
                left=x+(dx+l*sx)*scale;right=x+(dx+r*sx+top*slant)*scale
                band=y-upm*.17*scale
                # Sparse cuts inside the base, with clear accent/mark zones.
                for j in range(34 if size>160 else 10):
                    a=rng.uniform(left,right);c=band+rng.uniform(-size*.031,size*.031)
                    ln=rng.uniform(size*.023,size*.10);t=rng.uniform(.4,size*.006)
                    scratches.append(f'<path d="M{a},{c} l{ln},-{t/2} l-{ln*.25},{t} l-{ln*.78},{t/3} Z"/>')
                if rng.random()<.72 and size>=100:
                    for j in range(6):
                        a=right+rng.uniform(0,size*.035);c=band+rng.uniform(0,size*.09)
                        rad=rng.uniform(.7,size*.017)/(j*.3+1)
                        specks.append(f'<circle cx="{a}" cy="{c}" r="{rad}"/>')
        cursor+=pos.x_advance
    outlines=f'<g transform="translate({x},{y}) scale({scale},{-scale})">'+''.join(pieces)+'</g>'
    ident=f'clip{len(checks)}'
    return f'<defs><clipPath id="{ident}">{outlines}</clipPath></defs><g fill="{INK}">{outlines}</g><g clip-path="url(#{ident})" fill="{PAPER}">'+''.join(scratches)+f'</g><g fill="{INK}">'+''.join(specks)+'</g>'

def reference(x,y):
    ref=TTFont(REF);rgs=ref.getGlyphSet();cmap=ref.getBestCmap();cursor=0;parts=[]
    for c in 'Many Weatz':
        name=cmap[ord(c)];p=SVGPathPen(rgs);rgs[name].draw(p)
        parts.append(f'<path d="{p.getCommands()}" transform="translate({cursor},0)"/>')
        cursor+=ref['hmtx'][name][0]
    return f'<g fill="{INK}" transform="translate({x},{y}) scale(.098,-.098)">'+''.join(parts)+'</g>'

def save(name,body,h):
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="1800" height="{h}" viewBox="0 0 1800 {h}"><rect width="1800" height="{h}" fill="{PAPER}"/>'+body+'</svg>'
    (ROOT/f'{name}.svg').write_text(svg,encoding='utf-8')
    cairosvg.svg2png(bytestring=svg.encode(),write_to=str(ROOT/f'{name}.png'))

body=label('COLLECTION STUDY / MANY WEATZ + SINHALA / DESIGN 12',70,58,18,ACCENT)
body+=label('Expressive contrast. Clear Sinhala forms.',70,114,41,INK)
body+=reference(75,316)
body+=label('STYLE REFERENCE',1100,206,17,ACCENT)
body+=label('Maname anatomy + Many Weatz influence',1040,244,20)
body+=label('High contrast / flowing exits / broken ink',1040,279,20)
body+='<path d="M70 370 H1730" stroke="#dccbbb"/>'
body+=lettering('සිංහල අකුරු',195,647,250,1450)
# Separate display ornament: kept below descenders and marks.
body+=f'<path d="M178 646 C102 704 69 641 92 562 C108 507 151 477 171 501 C194 528 149 570 146 576 C176 527 179 506 166 501 C140 490 87 584 99 637 C108 676 145 667 178 646 Z M1354 678 C1454 734 1605 714 1673 626 C1706 583 1685 534 1658 549 C1627 566 1640 612 1660 602 C1653 600 1643 589 1648 577 C1660 541 1698 559 1689 591 C1661 695 1486 755 1354 678 Z" fill="{INK}"/>'
body+=label('WORDS / familiar forms at reading size',70,768,17,ACCENT)
body+=lettering('ලස්සන අකුරින් සිංහල ලියමු',90,883,109,1620)
body+=lettering('හදවත   සහන   ලහිරු   මහනුවර',90,1001,104,1620)
body+='<path d="M70 1052 H1730" stroke="#dccbbb"/>'
body+=label('HA / STANDARD FORM',80,1100,16,ACCENT)
body+=label('HA / PROPOSED STYLE',520,1100,16,ACCENT)
body+=lettering('හ',115,1289,221,290,False)
body+=lettering('හ',570,1289,221,290)
body+=lettering('හා  හි  හී',1010,1188,90,675)
body+=lettering('හු  හූ  හෙ  හේ',1010,1290,83,675)
body+=label('Recognition retained in the base and vowel combinations.',80,1343,17)
body+='<path d="M70 1373 H1730" stroke="#dccbbb"/>'
body+=label('Maname-derived design study / custom pen endings and ink texture / SVG preview, no new TTF',70,1412,16)
save('19-collection-sinhala-design',body,1460)

chars='අආඇඈඉඊඋඌඍඎඏඐඑඒඓඔඕඖකඛගඝඞඟචඡජඣඤඥඦටඨඩඪණඬතථදධනඳපඵබභමඹයරලවශෂසහළෆ'
body=label('SINHALA / COLLECTION DESIGN 12 / BASE-LETTER PROOF',65,61,18,ACCENT)
body+=label('The alphabet, with the same pen treatment.',65,116,37,INK)
body+=label('59 base letters / conventional forms retained / marks and contextual forms are a separate production stage',65,157,18)
for i,c in enumerate(chars):
    col=i%9;row=i//9;x=65+col*187;y=204+row*194
    body+=f'<rect x="{x}" y="{y}" width="175" height="180" rx="5" stroke="#e5d9cb" fill="none"/>'
    body+=lettering(c,x+14,y+122,117,142)
    body+=label(f'U+{ord(c):04X}',x+48,y+161,14)
body+=label('Design proof / Maname adaptation / no new font generated',65,1608,17)
save('20-collection-sinhala-alphabet',body,1650)
assert all(c['missing_glyphs']==0 for c in checks)
(ROOT/'design-12-notes.json').write_text(json.dumps({'basis':str(BASE),'reference':str(REF),'status':'Maname-derived vector design preview, not an original complete font','recognition':'Retains source Sinhala skeleton and HarfBuzz placement; proposed HA compared with standard HA','changes':'Maname high-contrast outlines, pointed exits, forward lean, ink texture, separate display swashes','checks':checks},ensure_ascii=False,indent=2),encoding='utf-8')
print(f'Created design and alphabet SVG/PNG; {len(checks)} runs without missing glyphs.')
