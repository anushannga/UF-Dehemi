"""Actual application line-breaking proof in isolated platform CI browsers.

Uses a fresh ephemeral Playwright Chromium context, served from localhost.
No user's browser profile, authentication, or installed font is accessed.
"""
from pathlib import Path
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread
import hashlib,json
from playwright.sync_api import sync_playwright
from build import VERSION,PREFIX,OUT

ROOT=Path(__file__).resolve().parent

class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self,*args):
        pass

def main():
    reports=ROOT/'qa';reports.mkdir(exist_ok=True)
    server=ThreadingHTTPServer(('127.0.0.1',0),partial(QuietHandler,directory=str(ROOT)))
    thread=Thread(target=server.serve_forever,daemon=True);thread.start()
    result={'version':VERSION,'status':'fail','font_hashes':{s:hashlib.sha256((OUT/f'{PREFIX}-{s}.ttf').read_bytes()).hexdigest() for s in ('Regular','Italic')}}
    try:
        with sync_playwright() as runtime:
            browser=runtime.chromium.launch(headless=True)
            try:
                page=browser.new_page(viewport={'width':1100,'height':1800},device_scale_factor=1)
                page.goto(f'http://127.0.0.1:{server.server_port}/documentation/browser-proof.html')
                page.wait_for_function("document.body.dataset.ready === 'true'")
                evidence=page.evaluate('window.softHyphenProof')
                result['browser']=browser.version
                result['evidence']=evidence
                page.screenshot(path=str(reports/f'browser-proof-{VERSION}.png'),full_page=True)
                assert evidence['status']=='executed-review-rendering',evidence
                assert evidence['loaded_faces']=={'Regular':1,'Italic':1}
                for style in ('Regular','Italic'):
                    wide=next(x for x in evidence['samples'] if x['style']==style and x['kind']=='wide')
                    narrow=next(x for x in evidence['samples'] if x['style']==style and x['kind']=='narrow')
                    assert wide['estimated_lines']==1 and all(x['width']==0 for x in wide['shy_rects']),(style,wide)
                    assert narrow['estimated_lines']==2 and any(x['width']>0 for x in narrow['shy_rects']),(style,narrow)
                result['status']='pass'
            finally:
                browser.close()
    finally:
        server.shutdown();server.server_close();thread.join(timeout=5)
        (reports/f'browser-validation-{VERSION}.json').write_text(json.dumps(result,indent=2),encoding='utf8')
    print(json.dumps(result))

if __name__=='__main__':
    main()
