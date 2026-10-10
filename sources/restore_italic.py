from pathlib import Path
import json,hashlib,zipfile
from fontTools.ttLib import TTFont
from PIL import Image,ImageDraw,ImageFont
import uharfbuzz as hb
import freetype
r=Path(__file__).resolve().parent;project=r.parent
source=project/'release-unicode/UF-Dehemi-Unicode-Regular.ttf'
original=project/'UF-Dehemi-Design12-Ink/UF-Dehemi-Final-Tight-232.ttf'
package=r/'UF-Dehemi-OFL-Italic-2.350';package.mkdir(exist_ok=True)
f=TTFont(source,recalcTimestamp=False)
notice='Copyright 2015-2023 The Maname Project Authors (https://github.com/mooniak/maname-font). UF-Dehemi modifications Copyright 2026 Pasan Anushanga. Release prepared for ANUSHANGA K P.'
names={0:notice,1:'UF-Dehemi OFL',2:'Italic',3:'2.350;UFDE;UF-Dehemi-OFL-Italic',4:'UF-Dehemi OFL Italic',5:'Version 2.350; original Tight-232 italic artwork restored',6:'UF-Dehemi-OFL-Italic',8:'ANUSHANGA K P',9:'Pasan Anushanga; The Maname Project Authors',10:'Original Tight-232 slanted display design, preserving glyphs, hinting and Sinhala layouts. Maname derivative under SIL OFL 1.1.',13:'This Font Software is licensed under the SIL Open Font License, Version 1.1. See OFL.txt.',14:'https://openfontlicense.org',16:'UF-Dehemi OFL',17:'Italic'}
for nid,value in names.items():
 f['name'].removeNames(nameID=nid)
 f['name'].setName(value,nid,3,1,0x409);f['name'].setName(value,nid,1,0,0)
f['OS/2'].fsType=0
f['OS/2'].fsSelection=(f['OS/2'].fsSelection|1)&~64
f['head'].macStyle=(f['head'].macStyle|2)&~1
f['head'].fontRevision=2.35
out=package/'UF-Dehemi-OFL-Italic.ttf';f.save(out)
check=TTFont(out,checkChecksums=2);old=TTFont(original)
for name in old.getGlyphOrder():
 a=old['glyf'][name];b=check['glyf'][name]
 assert a.getCoordinates(old['glyf'])==b.getCoordinates(check['glyf']),name
 assert getattr(a,'program',None).getBytecode()==getattr(b,'program',None).getBytecode() if hasattr(a,'program') else not hasattr(b,'program'),name
assert old['hmtx'].metrics==check['hmtx'].metrics
from io import BytesIO
from fontTools.misc.xmlWriter import XMLWriter
def xml(font,tag):
 stream=BytesIO();font[tag].toXML(XMLWriter(stream),font);return stream.getvalue()
for tag in ['GSUB','GPOS','GDEF']:assert xml(old,tag)==xml(check,tag),tag
for tag in ['fpgm','prep','cvt ']:
 if tag in old:assert old.getTableData(tag)==check.getTableData(tag),tag
assert old.getGlyphOrder()==check.getGlyphOrder()
samples=['ශ්‍රී ලංකාවේ සිංහල අකුරු','ක්‍රියාකාරී ප්‍රෞඩ සංස්කෘතිය','අ ආ ඇ ඈ ඉ ඊ උ ඌ ඍ ඎ ඏ ඐ එ ඒ ඓ ඔ ඕ ඖ','ක ඛ ග ඝ ඞ ච ඡ ජ ඣ ඤ ඥ ට ඨ ඩ ඪ ණ','ත ථ ද ධ න ප ඵ බ භ ම ය ර ල ව ශ ෂ ස හ ළ ෆ','කා කැ කෑ කි කී කු කූ කෘ කෙ කේ කෛ කො කෝ කෞ ක්','ක්‍ර ක්‍ය ශ්‍රී ක්ෂ','කො කො කෝ කෝ කෞ කෞ','English ABC abc 0123456789']
cm=old.getBestCmap();tests=samples+[chr(cp)+v for cp in range(0xD9A,0xDC7) if cp in cm for v in ['','ා','ැ','ෑ','ි','ී','ු','ූ','ෘ','ෲ','ෙ','ේ','ෛ','ො','ෝ','ෞ','්','්‍ර','්‍ය']]
def shape(path,text):
 hf=hb.Font(hb.Face(path.read_bytes()));b=hb.Buffer();b.add_str(text);b.guess_segment_properties();b.language='si';hb.shape(hf,b)
 return [(g.codepoint,p.x_advance,p.y_advance,p.x_offset,p.y_offset) for g,p in zip(b.glyph_infos,b.glyph_positions)]
for s in tests:
 a=shape(original,s);b=shape(out,s);assert a==b;assert all(g[0] for g in b)
face=freetype.Face(str(out))
for size in [12,16,24,48,96]:
 face.set_pixel_sizes(0,size)
 for gid in range(len(check.getGlyphOrder())):face.load_glyph(gid,freetype.FT_LOAD_RENDER)
report={'source':'UF-Dehemi-Final-Tight-232.ttf (internal 2.330)','glyph_count':len(check.getGlyphOrder()),'italic_angle':check['post'].italicAngle,'outlines_metrics_layout_hinting_identical':True,'shape_cases_identical':len(tests),'FreeType_renders_passed':len(check.getGlyphOrder())*5,'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'limitations':'Original artwork retained, including source contour warnings and absent U+0D81. No universal-platform certification.'}
(package/'VALIDATION.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
body=(project/'release-unicode/OFL.txt').read_text(encoding='utf-8');body=body[body.index('This Font Software is licensed'):]
(package/'OFL.txt').write_text(notice+'\n\n'+body,encoding='utf-8')
(package/'README.txt').write_text('''UF-DEHEMI OFL ITALIC 2.350
This restores the original Tight-232 italic-style design selected by the user.
All 1,086 glyphs, advances, hinting and Sinhala OpenType layout tables are
preserved exactly. This is the Maname-derived branch, not the separately
drawn Independent 3.000 or OFL 3.100 branch.

Install UF-Dehemi-OFL-Italic.ttf. Font family: UF-Dehemi OFL; style: Italic.
Distributed under SIL OFL 1.1. Retain OFL.txt and copyright notices when sharing.
Personal/commercial design use, modification and redistribution are allowed
under OFL conditions. Font software cannot be sold by itself.

Known source limitations: U+0D81 is absent, and original contour warnings
remain. No claim that the independent branch's zero-warning validation applies
to this restored design. Google Docs custom-font upload is not supported;
this release has not been submitted to or accepted by Google Fonts.
''',encoding='utf-8')
im=Image.new('RGB',(2000,1650),'#fffaf2');d=ImageDraw.Draw(im)
title=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',38)
d.text((60,30),'UF-Dehemi OFL Italic 2.350 — original Tight-232 artwork',font=title,fill='black')
for i,s in enumerate(samples):d.text((60,130+i*160),s,font=ImageFont.truetype(str(out),58,layout_engine=ImageFont.Layout.RAQM),fill='black',language='si')
im.save(package/'Preview.png')
zipout=r/'UF-Dehemi-OFL-Italic-2.350.zip'
with zipfile.ZipFile(zipout,'w',zipfile.ZIP_DEFLATED) as z:
 manifest={}
 for p in package.iterdir():
  if p.is_file():z.write(p,package.name+'/'+p.name);manifest[p.name]=hashlib.sha256(p.read_bytes()).hexdigest()
 z.writestr(package.name+'/SHA256SUMS.txt',''.join(f'{v}  {n}\n' for n,v in sorted(manifest.items())))
with zipfile.ZipFile(zipout) as z:assert z.testzip() is None
print(json.dumps(report,indent=2));print(zipout.resolve())
