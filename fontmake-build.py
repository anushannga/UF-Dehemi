"""UFO/fontmake development build; release layout is overlaid from canonical build.

This target intentionally does not overwrite release TTFs. Exported sources lose
TrueType hinting; compare this target before migrating the production release.
"""
from pathlib import Path
import subprocess, sys, copy, shutil, json
import uharfbuzz as hb
from fontTools.ttLib import TTFont
R=Path(__file__).resolve().parent
out=R/'build/fontmake';out.mkdir(parents=True,exist_ok=True)
report={}
def shape(path,text):
    font=hb.Font(hb.Face(path.read_bytes()));buffer=hb.Buffer();buffer.add_str(text);buffer.guess_segment_properties();buffer.language='si';hb.shape(font,buffer)
    return [(g.codepoint,p.x_advance,p.y_advance,p.x_offset,p.y_offset) for g,p in zip(buffer.glyph_infos,buffer.glyph_positions)]
for style in ['Regular','Italic']:
    target=out/f'UFDehemi-{style}.ttf'
    staged=out/f'UFDehemi-{style}.ufo'
    shutil.copytree(R/'sources'/f'UFDehemi-{style}.ufo',staged,dirs_exist_ok=True)
    # FontForge's reverse-export FEA uses syntax rejected by feaLib.
    # Compile outlines here; canonical TTX carries the authoritative layouts.
    (staged/'features.fea').write_text('',encoding='utf8')
    subprocess.run([sys.executable,'-m','fontmake','-u',str(staged),'-o','ttf','--output-path',str(target),'--keep-overlaps','--no-production-names'],check=True)
    fresh=TTFont(target);canonical=TTFont(R/'fonts/ttf/ufdehemi'/f'UFDehemi-{style}.ttf')
    from fontTools.ttLib.reorderGlyphs import reorderGlyphs
    assert set(fresh.getGlyphOrder())==set(canonical.getGlyphOrder())
    reorderGlyphs(fresh,canonical.getGlyphOrder())
    for tag in ['GSUB','GPOS','GDEF','name']:
        if tag in canonical:fresh[tag]=copy.deepcopy(canonical[tag])
    fresh.save(target)
    release=R/'fonts/ttf/ufdehemi'/f'UFDehemi-{style}.ttf'
    texts=['ශ්‍රී ලංකා','ක්‍රියා','ප්‍රශ්න','විද්‍යාව','න්‍යාය','ක්ෂේත්‍ර','අ\u0d81']
    texts += [chr(cp)+suffix for cp in range(0xd9a,0xdc7) if cp in canonical.getBestCmap() for suffix in ['','ා','ැ','ෑ','ි','ී','ු','ූ','ෘ','ෲ','ෙ','ේ','ෛ','ො','ෝ','ෞ','්','්‍ර','්‍ය']]
    for text in texts:assert shape(release,text)==shape(target,text),(style,text)
    report[style]={'matching_shaping_cases':len(texts),'limitations':'Fontmake development output is unhinted and is not pixel-identical to canonical release.'}
    print('Built UFO/fontmake development target:',target)
(R/'qa/fontmake-validation.json').write_text(json.dumps(report,indent=2),encoding='utf8')
