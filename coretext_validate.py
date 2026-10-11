"""Validate Dehemi with the real macOS CoreText shaper, without installation.

Run after build.py on a 64-bit macOS host: python coretext_validate.py.
The result is written only after an actual macOS run. A syntax check on Windows
does not execute CoreText and must not be described as a platform test passing.

Fonts are constructed from file-backed private descriptors. No font-registration
or system-installation API is called. Every shaped run must use the requested
PostScript font, so a system fallback font cannot silently make a test pass.

API ownership and signatures follow Apple's CoreFoundation/CoreText APIs:
https://developer.apple.com/documentation/technologyoverviews/fonts
https://developer.apple.com/documentation/coretext/ctrungetstringindices(_:_:_:)
"""

from __future__ import annotations

import ctypes as C
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import sys

from fontTools.ttLib import TTFont


ROOT = Path(__file__).resolve().parent
from build import OUT as FONT_DIR, VERSION, PREFIX
REPORT = ROOT / "qa" / f"coretext-validation-{VERSION}.json"
CASES = [
    "ශ්‍රී ලංකා", "ක්‍රියා", "ප්‍රශ්න", "විද්‍යාව", "න්‍යාය", "ක්ෂේත්‍ර",
    "ඇ ඈ", "අ\u0d81", "ක\u0d81", "\u25cc\u0d81",
]
SUFFIXES = [
    "", "ා", "ැ", "ෑ", "ි", "ී", "ු", "ූ", "ෘ", "ෲ", "ෙ", "ේ", "ෛ",
    "ො", "ෝ", "ෞ", "්", "්‍ර", "්‍ය",
]

# Darwin LP64 ABI: CFIndex is signed long, CGFloat is double and CGGlyph is
# unsigned short. Explicit signatures prevent ctypes' default int return type
# from truncating CoreFoundation object pointers.
CFIndex = C.c_long
CFRef = C.c_void_p
Boolean = C.c_uint8
CFStringEncoding = C.c_uint32
CGGlyph = C.c_uint16
CGFloat = C.c_double
UTF8 = 0x08000100


class CFRange(C.Structure):
    _fields_ = [("location", CFIndex), ("length", CFIndex)]


class CGPoint(C.Structure):
    _fields_ = [("x", CGFloat), ("y", CGFloat)]


class CGSize(C.Structure):
    _fields_ = [("width", CGFloat), ("height", CGFloat)]


class CGAffineTransform(C.Structure):
    _fields_ = [(n, CGFloat) for n in ("a", "b", "c", "d", "tx", "ty")]


class CFDictionaryKeyCallBacks(C.Structure):
    _fields_ = [
        ("version", CFIndex), ("retain", CFRef), ("release", CFRef),
        ("copyDescription", CFRef), ("equal", CFRef), ("hash", CFRef),
    ]


class CFDictionaryValueCallBacks(C.Structure):
    _fields_ = [
        ("version", CFIndex), ("retain", CFRef), ("release", CFRef),
        ("copyDescription", CFRef), ("equal", CFRef),
    ]


class CoreText:
    """Small C API binding; all Create/Copy references have explicit releases."""

    def __init__(self):
        if sys.platform != "darwin":
            raise RuntimeError("Actual CoreText validation requires macOS.")
        if C.sizeof(CFIndex) != 8 or C.sizeof(CFRef) != 8:
            raise RuntimeError("This harness supports the 64-bit macOS ABI only.")
        self.cf = C.CDLL(
            "/System/Library/Frameworks/CoreFoundation.framework/CoreFoundation"
        )
        self.ct = C.CDLL("/System/Library/Frameworks/CoreText.framework/CoreText")
        self._bind(self.cf, "CFRelease", None, CFRef)
        self._bind(self.cf, "CFArrayGetCount", CFIndex, CFRef)
        self._bind(self.cf, "CFArrayGetValueAtIndex", CFRef, CFRef, CFIndex)
        self._bind(
            self.cf, "CFURLCreateFromFileSystemRepresentation", CFRef,
            CFRef, C.POINTER(C.c_uint8), CFIndex, Boolean,
        )
        self._bind(
            self.cf, "CFStringCreateWithBytes", CFRef,
            CFRef, C.POINTER(C.c_uint8), CFIndex, CFStringEncoding, Boolean,
        )
        self._bind(self.cf, "CFStringGetLength", CFIndex, CFRef)
        self._bind(
            self.cf, "CFStringGetMaximumSizeForEncoding", CFIndex,
            CFIndex, CFStringEncoding,
        )
        self._bind(
            self.cf, "CFStringGetCString", Boolean,
            CFRef, C.POINTER(C.c_char), CFIndex, CFStringEncoding,
        )
        self._bind(
            self.cf, "CFDictionaryCreate", CFRef,
            CFRef, C.POINTER(CFRef), C.POINTER(CFRef), CFIndex,
            C.POINTER(CFDictionaryKeyCallBacks),
            C.POINTER(CFDictionaryValueCallBacks),
        )
        self._bind(self.cf, "CFDictionaryGetValue", CFRef, CFRef, CFRef)
        self._bind(self.cf, "CFAttributedStringCreate", CFRef, CFRef, CFRef, CFRef)
        self._bind(self.ct, "CTFontManagerCreateFontDescriptorsFromURL", CFRef, CFRef)
        self._bind(
            self.ct, "CTFontCreateWithFontDescriptor", CFRef,
            CFRef, CGFloat, C.POINTER(CGAffineTransform),
        )
        self._bind(self.ct, "CTFontCopyPostScriptName", CFRef, CFRef)
        self._bind(self.ct, "CTFontGetUnitsPerEm", C.c_uint32, CFRef)
        self._bind(self.ct, "CTLineCreateWithAttributedString", CFRef, CFRef)
        self._bind(self.ct, "CTLineGetGlyphRuns", CFRef, CFRef)
        self._bind(self.ct, "CTRunGetGlyphCount", CFIndex, CFRef)
        self._bind(self.ct, "CTRunGetAttributes", CFRef, CFRef)
        self._bind(self.ct, "CTRunGetStringRange", CFRange, CFRef)
        self._bind(self.ct, "CTRunGetGlyphs", None, CFRef, CFRange, C.POINTER(CGGlyph))
        self._bind(
            self.ct, "CTRunGetPositions", None,
            CFRef, CFRange, C.POINTER(CGPoint),
        )
        self._bind(
            self.ct, "CTRunGetAdvances", None,
            CFRef, CFRange, C.POINTER(CGSize),
        )
        self._bind(
            self.ct, "CTRunGetStringIndices", None,
            CFRef, CFRange, C.POINTER(CFIndex),
        )
        # These are exported CFStringRef variables, not the addresses of strings.
        self.font_key = CFRef.in_dll(self.ct, "kCTFontAttributeName").value
        self.language_key = CFRef.in_dll(self.ct, "kCTLanguageAttributeName").value
        self.key_callbacks = CFDictionaryKeyCallBacks.in_dll(
            self.cf, "kCFTypeDictionaryKeyCallBacks"
        )
        self.value_callbacks = CFDictionaryValueCallBacks.in_dll(
            self.cf, "kCFTypeDictionaryValueCallBacks"
        )

    @staticmethod
    def _bind(lib, name, restype, *argtypes):
        fn = getattr(lib, name)
        fn.restype = restype
        fn.argtypes = list(argtypes)

    def release(self, ref):
        if ref:
            self.cf.CFRelease(ref)

    @staticmethod
    def require(ref, operation):
        if not ref:
            raise RuntimeError(f"{operation} returned NULL")
        return ref

    def string(self, text):
        encoded = text.encode("utf-8")
        data = (C.c_uint8 * len(encoded)).from_buffer_copy(encoded)
        return self.require(
            self.cf.CFStringCreateWithBytes(None, data, len(encoded), UTF8, False),
            "CFStringCreateWithBytes",
        )

    def string_value(self, ref):
        length = self.cf.CFStringGetLength(ref)
        size = self.cf.CFStringGetMaximumSizeForEncoding(length, UTF8) + 1
        if size <= 0:
            raise RuntimeError("Invalid CoreFoundation string buffer size")
        buf = C.create_string_buffer(size)
        if not self.cf.CFStringGetCString(ref, buf, size, UTF8):
            raise RuntimeError("CFStringGetCString could not convert to UTF-8")
        return buf.value.decode("utf-8")

    def postscript_name(self, font):
        name = self.require(self.ct.CTFontCopyPostScriptName(font), "CTFontCopyPostScriptName")
        try:
            return self.string_value(name)
        finally:
            self.release(name)

    def private_font(self, path, expected_name, size):
        """Create from the specified file, never resolve by installed font name."""
        encoded = os.fsencode(path.resolve())
        data = (C.c_uint8 * len(encoded)).from_buffer_copy(encoded)
        url = self.require(
            self.cf.CFURLCreateFromFileSystemRepresentation(None, data, len(encoded), False),
            "CFURLCreateFromFileSystemRepresentation",
        )
        descriptors = None
        font = None
        try:
            descriptors = self.require(
                self.ct.CTFontManagerCreateFontDescriptorsFromURL(url),
                "CTFontManagerCreateFontDescriptorsFromURL",
            )
            count = self.cf.CFArrayGetCount(descriptors)
            if count != 1:
                raise RuntimeError(f"Expected one font face in {path}, found {count}")
            descriptor = self.cf.CFArrayGetValueAtIndex(descriptors, 0)
            font = self.require(
                self.ct.CTFontCreateWithFontDescriptor(descriptor, size, None),
                "CTFontCreateWithFontDescriptor",
            )
            actual_name = self.postscript_name(font)
            if actual_name != expected_name:
                raise AssertionError(
                    f"Requested file {path}: expected {expected_name}, got {actual_name}"
                )
            return font
        except BaseException:
            self.release(font)
            raise
        finally:
            self.release(descriptors)
            self.release(url)

    def shape(self, font, expected_name, text):
        string = language = attrs = attributed = line = None
        try:
            string = self.string(text)
            language = self.string("si")
            keys = (CFRef * 2)(self.font_key, self.language_key)
            values = (CFRef * 2)(font, language)
            attrs = self.require(
                self.cf.CFDictionaryCreate(
                    None, keys, values, 2,
                    C.byref(self.key_callbacks), C.byref(self.value_callbacks),
                ),
                "CFDictionaryCreate",
            )
            attributed = self.require(
                self.cf.CFAttributedStringCreate(None, string, attrs),
                "CFAttributedStringCreate",
            )
            line = self.require(
                self.ct.CTLineCreateWithAttributedString(attributed),
                "CTLineCreateWithAttributedString",
            )
            runs = self.require(self.ct.CTLineGetGlyphRuns(line), "CTLineGetGlyphRuns")
            result = []
            for index in range(self.cf.CFArrayGetCount(runs)):
                # Runs and attributes are borrowed references owned by the line.
                run = self.cf.CFArrayGetValueAtIndex(runs, index)
                attributes = self.ct.CTRunGetAttributes(run)
                actual_font = self.require(
                    self.cf.CFDictionaryGetValue(attributes, self.font_key),
                    "CTRun font attribute",
                )
                actual_name = self.postscript_name(actual_font)
                if actual_name != expected_name:
                    raise AssertionError(
                        f"Font fallback in {text!r}: expected {expected_name}, got {actual_name}"
                    )
                count = self.ct.CTRunGetGlyphCount(run)
                if count < 0:
                    raise RuntimeError("CoreText returned a negative glyph count")
                glyphs = (CGGlyph * count)()
                positions = (CGPoint * count)()
                advances = (CGSize * count)()
                indices = (CFIndex * count)()
                whole_run = CFRange(0, 0)
                if count:
                    self.ct.CTRunGetGlyphs(run, whole_run, glyphs)
                    self.ct.CTRunGetPositions(run, whole_run, positions)
                    self.ct.CTRunGetAdvances(run, whole_run, advances)
                    self.ct.CTRunGetStringIndices(run, whole_run, indices)
                text_range = self.ct.CTRunGetStringRange(run)
                shaped = []
                for i in range(count):
                    if glyphs[i] == 0:
                        raise AssertionError(
                            f"Missing glyph in {text!r}, UTF-16 string index {indices[i]}"
                        )
                    coords = (
                        positions[i].x, positions[i].y,
                        advances[i].width, advances[i].height,
                    )
                    if not all(math.isfinite(v) for v in coords):
                        raise AssertionError(f"Non-finite CoreText geometry in {text!r}")
                    shaped.append({
                        "glyph_id": int(glyphs[i]),
                        "utf16_index": int(indices[i]),
                        "position": [positions[i].x, positions[i].y],
                        "advance": [advances[i].width, advances[i].height],
                    })
                result.append({
                    "postscript_name": actual_name,
                    "utf16_range": [int(text_range.location), int(text_range.length)],
                    "glyphs": shaped,
                })
            if not any(run["glyphs"] for run in result):
                raise AssertionError(f"CoreText produced no glyphs for {text!r}")
            return result
        finally:
            # Reverse creation order. Dictionary/attributed string retain values.
            for ref in (line, attributed, attrs, language, string):
                self.release(ref)


def validate_style(api, style):
    path = FONT_DIR / f"{PREFIX}-{style}.ttf"
    expected_name = f"{PREFIX}-{style}"
    with TTFont(path) as source:
        cmap = source.getBestCmap()
        if source["name"].getDebugName(6) != expected_name:
            raise AssertionError(f"Unexpected source PostScript name in {path}")
        texts = CASES + [
            chr(cp) + suffix
            for cp in range(0xD9A, 0xDC7) if cp in cmap
            for suffix in SUFFIXES
        ]
        if len(texts) != 789:
            raise AssertionError(f"Expected the 789-case Windows corpus, got {len(texts)}")
        mark_id = source.getGlyphID(cmap[0xD81])
        upm = source["head"].unitsPerEm
        conjuncts = {
            "ක්\u200dෂ": [source.getGlyphID("sinKSsa")],
            "ක්\u200dර": [source.getGlyphID("sinKRa")],
            "ත්\u200dය": [source.getGlyphID("sinTa"), source.getGlyphID("sinYansaya")],
        }
    font = api.private_font(path, expected_name, upm)
    try:
        if api.ct.CTFontGetUnitsPerEm(font) != upm:
            raise AssertionError(f"CoreText/source units-per-em mismatch in {path}")
        run_names = set()
        mark_positions = {}
        for text in texts:
            shaped = api.shape(font, expected_name, text)
            run_names.update(run["postscript_name"] for run in shaped)
            if text in CASES[-3:]:
                glyphs = [g for run in shaped for g in run["glyphs"]]
                marks = [g for g in glyphs if g["glyph_id"] == mark_id]
                if not marks:
                    raise AssertionError(f"Chandrabindu not shaped in {style}: {text!r}")
                if any(abs(g["advance"][0]) > 1e-6 for g in marks):
                    raise AssertionError(f"Chandrabindu has nonzero advance: {style}, {text!r}")
                if text == "ක\u0d81" and not any(abs(g["position"][1]) > 1e-6 for g in marks):
                    raise AssertionError(f"Chandrabindu attachment has no vertical position: {style}")
                mark_positions[text] = shaped
        for text, expected in conjuncts.items():
            shaped = api.shape(font, expected_name, text)
            actual = [g["glyph_id"] for run in shaped for g in run["glyphs"]]
            if actual != expected:
                raise AssertionError(f"Conjunct substitution mismatch {style}, {text!r}: {actual} != {expected}")
        return {
            "status": "pass",
            "coretext_cases": len(texts),
            "postscript_name": expected_name,
            "actual_run_fonts": sorted(run_names),
            "no_missing_glyphs": True,
            "no_fallback_fonts": True,
            "expected_conjunct_cases": len(conjuncts),
            "font_size_points": upm,
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "mark_positions": mark_positions,
        }
    finally:
        api.release(font)


def main():
    if sys.platform != "darwin":
        raise SystemExit(
            "CoreText not executed: run this script on a 64-bit macOS CI runner. "
            "No CoreText pass report has been generated on this host."
        )
    result = {
        "version": VERSION,
        "engine": "Apple CoreText",
        "platform": platform.platform(),
        "architecture": platform.machine(),
        "private_font_loading": "file descriptors; no registration or installation",
        "styles": {},
        "limitations": (
            "Actual CoreText shaping and font fallback checks for this corpus. "
            "Does not certify every string, application, rasterizer or Google Docs availability."
        ),
    }
    try:
        api = CoreText()
        for style in ("Regular", "Italic"):
            result["styles"][style] = validate_style(api, style)
        result["status"] = "pass"
    except Exception as exc:
        result["status"] = "fail"
        result["error"] = f"{type(exc).__name__}: {exc}"
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
        print(json.dumps(result, ensure_ascii=True))
        raise
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=True))


if __name__ == "__main__":
    main()
