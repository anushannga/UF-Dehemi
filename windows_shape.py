"""Exercise Windows Uniscribe shaping with an isolated private test family."""
import ctypes as C
from ctypes import wintypes as W
from pathlib import Path
from fontTools.ttLib import TTFont
import json,sys,uuid

class Analysis(C.Structure): _fields_=[('flags',W.WORD),('state',W.WORD)]
class Item(C.Structure): _fields_=[('position',C.c_int),('analysis',Analysis)]
class Offset(C.Structure): _fields_=[('du',C.c_int),('dv',C.c_int)]
class ABC(C.Structure): _fields_=[('a',C.c_int),('b',C.c_uint),('c',C.c_int)]

gdi=C.WinDLL('gdi32'); usp=C.WinDLL('usp10')
gdi.CreateCompatibleDC.argtypes=[C.c_void_p]; gdi.CreateCompatibleDC.restype=C.c_void_p
gdi.CreateFontW.argtypes=[C.c_int]*5+[W.DWORD]*8+[W.LPCWSTR]; gdi.CreateFontW.restype=C.c_void_p
gdi.SelectObject.argtypes=[C.c_void_p,C.c_void_p]; gdi.SelectObject.restype=C.c_void_p
gdi.AddFontResourceExW.argtypes=[W.LPCWSTR,W.DWORD,C.c_void_p]; gdi.AddFontResourceExW.restype=C.c_int
gdi.RemoveFontResourceExW.argtypes=[W.LPCWSTR,W.DWORD,C.c_void_p]
gdi.DeleteObject.argtypes=[C.c_void_p]; gdi.DeleteDC.argtypes=[C.c_void_p]
gdi.GetTextFaceW.argtypes=[C.c_void_p,C.c_int,W.LPWSTR];gdi.GetTextFaceW.restype=C.c_int
usp.ScriptItemize.argtypes=[W.LPCWSTR,C.c_int,C.c_int,C.c_void_p,C.c_void_p,C.POINTER(Item),C.POINTER(C.c_int)]
usp.ScriptShape.argtypes=[C.c_void_p,C.POINTER(C.c_void_p),W.LPCWSTR,C.c_int,C.c_int,C.POINTER(Analysis),C.POINTER(W.WORD),C.POINTER(W.WORD),C.POINTER(W.WORD),C.POINTER(C.c_int)]
usp.ScriptPlace.argtypes=[C.c_void_p,C.POINTER(C.c_void_p),C.POINTER(W.WORD),C.c_int,C.POINTER(W.WORD),C.POINTER(Analysis),C.POINTER(C.c_int),C.POINTER(Offset),C.POINTER(ABC)]
usp.ScriptFreeCache.argtypes=[C.POINTER(C.c_void_p)]

def check(result):
    if result<0: raise RuntimeError(f'Windows shaping HRESULT 0x{result & 0xffffffff:08X}')

class WindowsShaper:
    def __init__(self,path):
        source=TTFont(path,recalcBBoxes=False,recalcTimestamp=False)
        self.family='UFQ'+uuid.uuid4().hex[:12]
        for nid in [1,4,6,16,21]:
            for record in source['name'].names:
                if record.nameID==nid: record.string=self.family.encode(record.getEncoding())
        self.path=Path(__file__).resolve().parent/'build/windows-private'/('private-'+self.family+'.ttf')
        self.path.parent.mkdir(parents=True,exist_ok=True)
        source.save(self.path)
        source.close()
        self.source=TTFont(path)
        assert gdi.AddFontResourceExW(str(self.path.resolve()),0x10,None)>0
        self.dc=gdi.CreateCompatibleDC(None)
        self.font=gdi.CreateFontW(-1000,0,0,0,400,int(self.source['post'].italicAngle!=0),0,0,1,0,0,0,0,self.family)
        self.previous=gdi.SelectObject(self.dc,self.font)
        selected=C.create_unicode_buffer(64)
        assert gdi.GetTextFaceW(self.dc,64,selected)>0 and selected.value==self.family,selected.value
        self.cache=C.c_void_p()
    def shape(self,text):
        items=(Item*20)(); count=C.c_int()
        check(usp.ScriptItemize(text,len(text),19,None,None,items,C.byref(count)))
        out=[]
        for i in range(count.value):
            segment=text[items[i].position:items[i+1].position]
            maxglyphs=3*len(segment)+20
            glyphs=(W.WORD*maxglyphs)(); clusters=(W.WORD*len(segment))(); attributes=(W.WORD*maxglyphs)(); n=C.c_int()
            analysis=items[i].analysis
            check(usp.ScriptShape(self.dc,C.byref(self.cache),segment,len(segment),maxglyphs,C.byref(analysis),glyphs,clusters,attributes,C.byref(n)))
            advances=(C.c_int*maxglyphs)(); offsets=(Offset*maxglyphs)(); abc=ABC()
            check(usp.ScriptPlace(self.dc,C.byref(self.cache),glyphs,n.value,attributes,C.byref(analysis),advances,offsets,C.byref(abc)))
            out.extend((glyphs[j],advances[j],offsets[j].du,offsets[j].dv) for j in range(n.value))
        return out
    def close(self):
        usp.ScriptFreeCache(C.byref(self.cache))
        gdi.SelectObject(self.dc,self.previous); gdi.DeleteObject(self.font); gdi.DeleteDC(self.dc)
        gdi.RemoveFontResourceExW(str(self.path.resolve()),0x10,None)
        self.source.close()
        try:self.path.unlink()
        except PermissionError:pass

if __name__=='__main__':
    shaper=WindowsShaper(Path(sys.argv[1]))
    try:
        for text in ['කො','කෝ','කේ','කෞ','ලෝ','ඩෝ','අඩෝ','රැ','රෑ','රු','රූ','ප්‍රෝ']:
            out=shaper.shape(text)
            print(ascii(text),[(shaper.source.getGlyphName(g),a,x,y) for g,a,x,y in out])
    finally: shaper.close()
