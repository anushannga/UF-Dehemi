"""Reconstruct historical geometry and hint programs in build/history-replay.

This is a current verification recipe, not a recovered historical command log.
It never replaces canonical source or release fonts.
"""
from pathlib import Path
import ast, contextlib, hashlib, importlib.util, io, json, sys
from fontTools.ttLib import TTFont
import ttfautohint
from importlib import metadata as package_metadata

HISTORY=Path(__file__).resolve().parent
ROOT=HISTORY.parent.parent
ORIGINAL=HISTORY/'original'
OUTPUT=ROOT/'build/history-replay'

def sha(data):return hashlib.sha256(data).hexdigest()
def fingerprint(font):
    encoded=lambda data:json.dumps(data,sort_keys=True,separators=(',',':')).encode()
    outlines={};hints={}
    for name in font.getGlyphOrder():
        glyph=font['glyf'][name];coords,endpoints,flags=glyph.getCoordinates(font['glyf'])
        outlines[name]=[list(coords),list(endpoints),list(flags)]
        hints[name]=glyph.program.getBytecode().hex() if hasattr(glyph,'program') else ''
    layout={}
    for tag in ['GSUB','GPOS','GDEF']:
        stream=io.StringIO();font.saveXML(stream,tables=[tag]);layout[tag]=sha(stream.getvalue().encode())
    return {'glyphs':len(font.getGlyphOrder()),'outlines':sha(encoded(outlines)),'metrics':sha(encoded(font['hmtx'].metrics)),'cmap':sha(encoded(font.getBestCmap())),'layout':layout,'glyph_programs':sha(encoded(hints)),'hint_tables':{t:sha(font.getTableData(t)) for t in ['fpgm','prep','cvt '] if t in font}}

def main():
    OUTPUT.mkdir(parents=True,exist_ok=True)
    manifest=json.loads((HISTORY/'script-manifest.json').read_text(encoding='utf8'))
    for name,record in manifest.items():
        assert sha((ORIGINAL/name).read_bytes())==record['sha256'],name
    maname=HISTORY/'inputs/Maname-Distributed-v2.ttf'
    assert sha(maname.read_bytes())=='8e616ff912bf881ffafbf032c9b80a46d0200c6037271352871d526b3be3f24f'
    baselines=json.loads((HISTORY/'baseline-fingerprints.json').read_text(encoding='utf8'))
    sys.path.insert(0,str(ORIGINAL))
    def load(name):
        spec=importlib.util.spec_from_file_location(name,ORIGINAL/f'{name}.py')
        module=importlib.util.module_from_spec(spec);sys.modules[name]=module
        spec.loader.exec_module(module);return module
    def run(module):
        with contextlib.redirect_stdout(io.StringIO()):module.main()
    def verify(name,path):
        actual=fingerprint(TTFont(path));expected=baselines[name]['fingerprint']
        assert all(actual[k]==expected[k] for k in ['glyphs','outlines','metrics','cmap','layout']),(name,'geometry/layout differs')
        return {'glyphs':actual['glyphs'],'geometry_metrics_cmap_layout_identical':True,'replayed_sha256':sha(path.read_bytes())}

    # Inspect only the Maname-based alphabet functions, never reference() or
    # preview-writing code. Many Weatz is not loaded or distributed here.
    tree=ast.parse((ORIGINAL/'build_collection_v12.py').read_text(encoding='utf8'))
    nodes=[]
    for node in tree.body:
        if getattr(node,'lineno',1000)>=21:continue
        if isinstance(node,ast.Import) and any(x.name=='cairosvg' for x in node.names):continue
        if isinstance(node,ast.Assign) and any(isinstance(x,ast.Name) and x.id in {'BASE','REF'} for x in node.targets):continue
        nodes.append(node)
    nodes += [n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in {'label','lettering'}]
    scope={'__file__':str(ORIGINAL/'build_collection_v12.py'),'BASE':maname}
    exec(compile(ast.Module(body=nodes,type_ignores=[]),'verified-historical-alphabet','exec'),scope)
    import xml.etree.ElementTree as ET
    chars='අආඇඈඉඊඋඌඍඎඏඐඑඒඓඔඕඖකඛගඝඞඟචඡජඣඤඥඦටඨඩඪණඬතථදධනඳපඵබභමඹයරලවශෂසහළෆ'
    paths={};fragments=[]
    for c in chars:
        fragment=scope['lettering'](c,0,0,117,142);fragments.append(fragment)
        element=ET.fromstring('<svg>'+fragment+'</svg>')
        ink=next(x for x in element if x.tag=='g' and x.get('fill')=='#211c20')
        paths[f'{ord(c):04X}']=' '.join(x.get('d') for g in ink if g.tag=='g' for x in g if x.tag=='path')
    assert paths==json.loads((ROOT/'sources/design12_glyph_paths.json').read_text(encoding='utf8'))
    reference=OUTPUT/'reference';reference.mkdir(exist_ok=True)
    (reference/'20-collection-sinhala-alphabet.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg">'+''.join(fragments)+'</svg>',encoding='utf8')
    prod=load('build_design12_production');prod.SOURCE=maname
    prod.PATHS=ROOT/'sources/design12_glyph_paths.json';prod.ROOT=reference
    prod.PROJECT=ROOT;prod.OUTDIR=OUTPUT/'production';prod.OUTPUT=prod.OUTDIR/'UF-Dehemi.ttf'
    run(prod);results={'production':verify('production',prod.OUTPUT)}
    texture=load('build_design12_ink');texture.SOURCE=prod.OUTPUT
    texture.OUTDIR=OUTPUT/'ink';texture.OUTPUT=texture.OUTDIR/'UF-Dehemi-Ink.ttf';run(texture)
    cleanup=load('clean_design12_ink_fragments');cleanup.FONT_PATH=texture.OUTPUT
    cleanup.REPORT=OUTPUT/'fragment-cleanup.json';run(cleanup);results['ink']=verify('ink',texture.OUTPUT)
    tails=load('remove_design12_hair_tails');tails.SOURCE=maname
    tails.SOURCE_FONT=texture.OUTPUT;tails.FONT_PATH=texture.OUTDIR/'UF-Dehemi-Ink-Clean.ttf'
    tails.REPORT=OUTPUT/'tails.json';run(tails);results['clean']=verify('clean',tails.FONT_PATH)
    metrics=load('finalize_design12_metrics');metrics.SOURCE=tails.FONT_PATH;metrics.ROOT=ROOT
    metrics.OUTPUT=texture.OUTDIR/'UF-Dehemi-Final.ttf';metrics.REPORT=OUTPUT/'metrics.json'
    run(metrics);results['final']=verify('final',metrics.OUTPUT)
    hinted=TTFont(io.BytesIO(ttfautohint.ttfautohint(in_buffer=metrics.OUTPUT.read_bytes())))
    expected=baselines['final']['fingerprint'];actual=fingerprint(hinted)
    assert actual['glyph_programs']==expected['glyph_programs'] and actual['hint_tables']==expected['hint_tables']
    # Reconstructed 80-unit sin* reduction then the observed seven-unit change
    # across positive-advance Sinhala glyphs, including ten Sinhala digits.
    for name in hinted.getGlyphOrder():
        width,lsb=hinted['hmtx'].metrics[name]
        if name.startswith('sin') and width>0:hinted['hmtx'].metrics[name]=(max(1,width-80),lsb)
    sinhala={n for n in hinted.getGlyphOrder() if n.startswith('sin')}
    sinhala.update(n for cp,n in hinted.getBestCmap().items() if 0x0D80<=cp<=0x0DFF)
    changed=0
    for name in sinhala:
        width,lsb=hinted['hmtx'].metrics[name]
        if width>0:hinted['hmtx'].metrics[name]=(max(1,width-7),lsb);changed+=1
    assert changed==513
    target=OUTPUT/'reconstructed-Tight2330.ttf';hinted.save(target)
    results['tight2330']=verify('tight2330',target)
    actual=fingerprint(TTFont(target));expected=baselines['tight2330']['fingerprint']
    assert actual['glyph_programs']==expected['glyph_programs'] and actual['hint_tables']==expected['hint_tables']
    canonical=TTFont(recalcTimestamp=False);canonical.importXML(ROOT/'sources/Upstream-Tight232.ttx')
    assert fingerprint(canonical)==expected,'Committed canonical stage differs'
    report={'scope':'Current reconstruction; not certification of original acquisition/commands or exclusive authorship','maname_input_sha256':sha(maname.read_bytes()),'alphabet_paths_reproduced':59,'many_weatz_input_loaded':False,'stages':results,'tight2330_glyph_programs_and_hint_tables_identical':True,'canonical_ttx_stage_fingerprint_identical':True,'spacing_glyphs_changed':changed,'dependencies':{}}
    for name in ['fonttools','skia-pathops','uharfbuzz','svgpathtools','ttfautohint-py']:
        report['dependencies'][name]=package_metadata.version(name)
    report['hint_tool']=ttfautohint.run(['--version'],capture_output=True,text=True).stdout.splitlines()[0]
    (ROOT/'qa/history-replay-2.441.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf8')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
