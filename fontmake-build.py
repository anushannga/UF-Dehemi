"""UFO/fontmake development build using editable native feature source.

This target intentionally does not overwrite release TTFs. Exported sources lose
TrueType hinting; compare this target before migrating the production release.
"""
from pathlib import Path
import subprocess, sys, shutil, json, hashlib, unicodedata
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from native_features import compile_features,unskew_positioning
from latin_extensions import add_latin_extensions,apply_latin_positioning,CARON_BASES,AUXILIARY_CODEPOINTS
from sinhala_marks import attach_virama_to_dotted_circle
from build import attach_chandrabindu,configure_metadata,PREFIX,OUT,VERSION
from math import tan,radians
R=Path(__file__).resolve().parent
out=R/'build/fontmake';out.mkdir(parents=True,exist_ok=True)
report={}
def shape(path,text,language='si'):
    font=hb.Font(hb.Face(path.read_bytes()));buffer=hb.Buffer();buffer.add_str(text);buffer.guess_segment_properties();buffer.language=language;hb.shape(font,buffer)
    return [(g.codepoint,p.x_advance,p.y_advance,p.x_offset,p.y_offset) for g,p in zip(buffer.glyph_infos,buffer.glyph_positions)]
for style in ['Regular','Italic']:
    target=out/f'{PREFIX}-{style}.ttf'
    staged=out/f'{PREFIX}-{style}.ufo'
    shutil.copytree(R/'sources'/f'{PREFIX}-{style}.ufo',staged,dirs_exist_ok=True)
    shutil.copy2(R/'sources/features.fea',staged/'features.fea')
    subprocess.run([sys.executable,'-m','fontmake','-u',str(staged),'-o','ttf','--output-path',str(target),'--keep-overlaps','--no-production-names'],check=True)
    fresh=TTFont(target);canonical=TTFont(OUT/f'{PREFIX}-{style}.ttf')
    from fontTools.ttLib.reorderGlyphs import reorderGlyphs
    assert set(fresh.getGlyphOrder())==set(canonical.getGlyphOrder())
    reorderGlyphs(fresh,canonical.getGlyphOrder())
    # Compile the same maintained FEA and source-declared language policy as
    # canonical build. No layout table is copied from a compiled font.
    compile_features(fresh)
    reference=TTFont(recalcTimestamp=False);reference.importXML(R/'sources/Upstream-Tight232.ttx')
    compile_features(reference)
    add_latin_extensions(reference)
    attach_chandrabindu(fresh,reference)
    apply_latin_positioning(fresh,reference=reference)
    attach_virama_to_dotted_circle(fresh,reference=reference)
    if style=='Regular':unskew_positioning(fresh,tan(radians(-14)))
    configure_metadata(fresh,style)
    from caron_components import componentize_alt_carons
    componentize_alt_carons(fresh)
    from discretionary_hyphen import configure_discretionary_hyphen
    configure_discretionary_hyphen(fresh)
    fresh.save(target)
    release=OUT/f'{PREFIX}-{style}.ttf'
    assert fresh.getBestCmap()==canonical.getBestCmap(),(style,'cmap mismatch')
    texts=['ශ්‍රී ලංකා','ක්‍රියා','ප්‍රශ්න','විද්‍යාව','න්‍යාය','ක්ෂේත්‍ර','අ\u0d81','ක\u0d81','◌\u0d81','◌්']
    texts += [chr(cp)+suffix for cp in range(0xd9a,0xdc7) if cp in canonical.getBestCmap() for suffix in ['','ා','ැ','ෑ','ි','ී','ු','ූ','ෘ','ෲ','ෙ','ේ','ෛ','ො','ෝ','ෞ','්','්‍ර','්‍ය']]
    for text in texts:assert shape(release,text)==shape(target,text),(style,text)
    latin_texts=[chr(cp) for cp in AUXILIARY_CODEPOINTS]
    latin_texts += [unicodedata.normalize('NFD',chr(cp)) for cp in CARON_BASES]
    latin_texts += ['l\u0303']
    for text in latin_texts:assert shape(release,text,'lt')==shape(target,text,'lt'),(style,text,'Latin layout mismatch')
    report[style]={'version':VERSION,'matching_shaping_cases':len(texts),'matching_latin_cases':len(latin_texts),'identical_cmap':True,'canonical_sha256':hashlib.sha256(release.read_bytes()).hexdigest(),'development_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'limitations':'Fontmake development output is unhinted and is not pixel-identical to canonical release.'}
    print('Built UFO/fontmake development target:',target)
(R/'qa/fontmake-validation.json').write_text(json.dumps(report,indent=2),encoding='utf8')
