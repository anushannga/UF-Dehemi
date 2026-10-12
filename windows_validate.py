"""Private Windows Uniscribe regression; does not install release fonts."""
from pathlib import Path
import json
from windows_shape import WindowsShaper
from build import VERSION,PREFIX,OUT
R=Path(__file__).resolve().parent
cases=['ශ්‍රී ලංකා','ක්‍රියා','ප්‍රශ්න','විද්‍යාව','න්‍යාය','ක්ෂේත්‍ර','ඇ ඈ','අ\u0d81','ක\u0d81','\u25cc\u0d81','◌්']
suffixes=['','ා','ැ','ෑ','ි','ී','ු','ූ','ෘ','ෲ','ෙ','ේ','ෛ','ො','ෝ','ෞ','්','්‍ර','්‍ය']
result={}
for style in ['Regular','Italic']:
    shaper=WindowsShaper(OUT/f'{PREFIX}-{style}.ttf')
    try:
        texts=cases+[chr(cp)+suffix for cp in range(0xd9a,0xdc7) if cp in shaper.source.getBestCmap() for suffix in suffixes]
        for text in texts:
            shaped=shaper.shape(text)
            assert shaped and all(g[0]!=0 for g in shaped),(style,ascii(text),shaped)
        chandra_cases=[t for t in cases if '\u0d81' in t]
        marks={ascii(t):shaper.shape(t) for t in chandra_cases}
        markid=shaper.source.getGlyphID('sinChandrabindu')
        for text in chandra_cases:assert any(g[0]==markid for g in shaper.shape(text)),(style,text)
        virama=shaper.source.getGlyphID('sinVirama');virama_output=shaper.shape('◌්')
        assert any(g[0]==virama and g[1]==0 and (g[2] or g[3]) for g in virama_output),(style,virama_output)
        result[style]={'windows_uniscribe_cases':len(texts),'mark_positions':marks,'dotted_circle_virama':virama_output,'limitations':'No CoreText, DirectWrite or every-app certification.'}
    finally:shaper.close()
(R/'qa'/f'windows-validation-{VERSION}.json').write_text(json.dumps(result,indent=2),encoding='utf8')
print(json.dumps(result))
