# Dehemi

Dehemi is a Sinhala Unicode display family with Regular and Italic styles under SIL Open Font License 1.1. Current version: **2.430**. The repository URL retains its historical `UF-Dehemi` name.

Italic preserves the original Tight-232 artwork and TrueType hints. Regular removes the italic shear from outlines and positioning anchors, with bounded outline corrections; it is unhinted. Choose **Dehemi Italic** for the original slanted design.

## Release and verification

Release files: `fonts/ttf/dehemi/Dehemi-Regular.ttf` and `fonts/ttf/dehemi/Dehemi-Italic.ttf`.

Version 2.430 fixes virama spacing and dotted-circle attachment, adds 18 auxiliary Latin characters, repairs Lithuanian `l` + tilde positioning, and aligns hhea/typo line metrics. Regular winding and nearly axial line segments are corrected, and proven degenerate segments are removed. Existing Italic coordinates and glyph hint instructions remain unchanged.

The shared default line height changes from 1553 to 1500 design units (about **3.4% less spacing**); existing documents may reflow. The measured glyph envelope remains -319 to 1154, within typo/hhea metrics -333 to 1167. Windows clipping margins remain -359 to 1194. This is tested coverage, not a claim for arbitrary stacks of combining marks.

Fontspector 1.9.0, unmodified Google Fonts profile, both styles: **204 PASS, 19 WARN, 0 FAIL, 137 SKIP, 13 INFO**. The 2.420 baseline had 196 PASS and 27 WARN. No checks are excluded and warnings are not relabeled as passes. Reports: [JSON](qa/fontspector-2.430.json), [HTML](qa/fontspector-2.430.html), [resolution record](qa/warning-resolution-2.430.json), [warning review](documentation/WARNING-REVIEW.md).

Local checks pass 788 HarfBuzz Sinhala cases and 5,540 FreeType glyph renders per style, plus 10 Latin NFC/NFD comparisons and targeted mark assertions. Windows Uniscribe passes 790 cases per style. Native UFO/fontmake builds match 789 Sinhala and 29 Latin cases per style and the complete cmap. Reports are in `qa/validation-2.430.json`, `qa/windows-validation-2.430.json` and `qa/fontmake-validation-2.430.json`.

The original 1,090 Italic glyphs have identical point coordinates and hint instructions to 2.420; 5,450 old-glyph raster comparisons are identical. Regular corrections move 515 points across 270 old glyphs by at most three design units. Existing advances change only for `sinVirama` (237 to zero); tested normal Sinhala shaping stays unchanged. See [outline QA](qa/outline-review-2.430.json) and [visual proof](documentation/outline-proof-2.430.png).

All Linux, Windows and macOS jobs passed in [run 38226501752](https://github.com/anushannga/UF-Dehemi/actions/runs/38226501752), testing `574efaca4d82c4ab0604663d703ad9c01e3f9c3f`. Canonical TTF hashes from all three platforms match the current release. Windows Uniscribe and actual macOS CoreText each pass 790 coverage cases per style; CoreText also passes three expected conjunct cases per style with no missing/fallback glyphs and mark-geometry checks. Linux Chromium 153.0.8010.12 passes the conditional soft-hyphen line-breaking proof in both styles. Reports: `qa/platform-validation-2.430.json`, `qa/coretext-validation-2.430.json`, `qa/browser-validation-2.430.json` and `qa/platforms/`.

## Build

Use Python 3.12 and pinned dependencies:

```sh
pip install -r requirements.txt
python build.py
python validate.py
python fontmake-build.py
```

The canonical build reads `sources/Upstream-Tight232.ttx`, preserves original Italic outlines/hints, and compiles maintained `sources/features.fea` with fontTools feaLib. `latin_extensions.py` and `sinhala_marks.py` generate source-defined glyph/positioning additions. `outline_cleanup.py` applies the bounded Regular correction. No binary layout table is copied from a compiled release.

SFD/UFO outlines are reverse exports, not the original drawing workflow. The FEA began as a reverse export and is now maintained, editable compiler input. `fontmake-build.py` builds UFO outlines/features, adds the same source-defined positioning and metadata, and compares layouts against the canonical release. Its outputs in `build/fontmake/` are unhinted and are not pixel-identical to the canonical TTFs.

The CI workflow builds on Linux, Windows and macOS. It runs native Windows Uniscribe and macOS CoreText checks on their actual platforms. Linux additionally executes `browser_validate.py` with an isolated Playwright Chromium context; it checks conditional soft-hyphen line breaking using the release TTFs. This does not access a user's browser profile.

## Attribution and onboarding

Dehemi derives from Maname. Upstream copyright and SIL OFL 1.1 terms are retained in [OFL.txt](OFL.txt) and the fonts. Pasan Anushanga is credited for modifications; ANUSHANGA K P is the supplied release preparer name. OpenAI Codex assisted with technical adjustments, the upright transformation, source preparation and QA. Exclusive ownership of upstream work is not claimed.

Continue [Google Fonts submission #11099](https://github.com/google/fonts/issues/11099). The selected name Dehemi removes the previous UF abbreviation issue. Human CLA, upstream contributor coverage and curator design/serving review remain pending. See [onboarding](documentation/ONBOARDING.md) and the [serving coverage proposal](documentation/SUBSET-COVERAGE-PROPOSAL.md).

OFL distribution permits use and redistribution under the license. A public release and successful checks do not constitute Google Fonts acceptance or guarantee Google Docs availability. [Official onboarding guide](https://googlefonts.github.io/gf-guide/onboarding.html).
