# Dehemi 2.440 current update

207 PASS, 8 WARN, 0 FAIL, 137 SKIP, 15 INFO. Eleven of the 19 prior warning messages are resolved. The remaining eight design/convention/serving warnings are disclosed in WARNING-REVIEW.md; curator acceptance and human contributor work are pending.

All Linux, Windows and macOS jobs passed in [run 38231411379](https://github.com/anushannga/UF-Dehemi/actions/runs/38231411379), at `6dc1621fc01401ffc11b6b8055a1b5f3dc6817f6`. The canonical font hashes from all platforms match the current release. Actual isolated Chromium conditional-hyphen checks pass on all three operating systems; native Windows Uniscribe and macOS CoreText checks also pass. Reports: `qa/platform-validation-2.440.json`, `qa/coretext-validation-2.440.json`, `qa/platforms/*-browser-validation-2.440.json`.

Download: https://github.com/anushannga/UF-Dehemi/releases/tag/v2.440 (verify publication before posting).

The prior 2.430 preparation text below is historical baseline evidence.

---

# Existing Google Fonts submission: Dehemi 2.430 update draft

Status: preparation draft for [google/fonts#11099](https://github.com/google/fonts/issues/11099). Verify the release and CI run links before posting this update; this file does not itself submit or approve the font.

Family: **Dehemi**

Styles: **Regular and Italic**, version **2.430**

Public source repository: https://github.com/anushannga/UF-Dehemi

Release preparer/contact: **ANUSHANGA K P**, GitHub **anushannga**. Pasan Anushanga is credited for the historical modifications; upstream Maname authors are credited in the license and fonts.

License: **SIL Open Font License 1.1**, with upstream Maname copyright retained.

## Proposed update

The author has selected the family name **Dehemi**, replacing UF Dehemi and removing the abbreviation issue. The earlier naming-exception request can be withdrawn. This is an update to the existing submission.

Version 2.430 fixes virama spacing/dotted-circle attachment, adds 18 auxiliary Latin characters, corrects Lithuanian l+tilde positioning, aligns hhea/typo line metrics and applies bounded Regular outline cleanup. Earlier macron/naming/chandrabindu fixes are retained. Default line height decreases from 1553 to 1500 design units (about 3.4%), so existing documents may reflow. Existing Tight-232 italic outlines and glyph hint instructions are preserved. The Regular companion removes the italic shear from both outlines and positioning anchors, and needs human design review.

The canonical build retains the TTX outline/hint source and compiles maintained native FEA. The UFO/fontmake development target compiles editable features directly and checks shaping parity; it does not overlay binary layout tables. SFD/UFO outlines and the initial FEA were reverse exports, and that source history remains documented. The development fontmake outputs are unhinted and not pixel-identical to the canonical release.

Local 2.430 validation records 788 HarfBuzz shaping cases and 5,540 FreeType glyph renders per style, with Sinhala coverage, metadata and mark-attachment assertions. Existing italic artwork and tested Sinhala shaping remain unchanged.

Fontspector 1.9.0 Google Fonts profile, both 2.430 styles: **204 PASS, 19 WARN, 0 FAIL, 137 SKIP and 13 INFO**. Reports: `qa/fontspector-2.430.json` and `qa/fontspector-2.430.html`. Language, spacing-mark, line-metric and Regular semi-vertical/direction checks pass. Remaining manual design, original hinted Italic and serving-coverage warnings are disclosed in WARNING-REVIEW.md; zero failures does not imply all checks passed.

Windows Uniscribe validation passes **790 shaping cases per style**; report: `qa/windows-validation-2.430.json`. This result is separate from HarfBuzz/FreeType tests and does not certify all Windows applications or DirectWrite behavior.

All Linux, Windows and macOS jobs passed in [run 38226501752](https://github.com/anushannga/UF-Dehemi/actions/runs/38226501752), testing `574efaca4d82c4ab0604663d703ad9c01e3f9c3f`. Canonical TTF hashes from all three platforms match the current release. Windows Uniscribe and actual macOS CoreText each pass 790 coverage cases per style; CoreText also passes three expected conjunct cases per style with no missing/fallback glyphs and mark-geometry checks. Linux Chromium 153.0.8010.12 passes the conditional soft-hyphen line-breaking proof in both styles. Reports: `qa/platform-validation-2.430.json`, `qa/coretext-validation-2.430.json`, `qa/browser-validation-2.430.json` and `qa/platforms/`.

Contributor agreements, upstream contributor coverage, curator design review and warning review remain pending. The Maname-derived source attribution is retained, and exclusive ownership is not claimed. Google Fonts acceptance and Google Docs availability are not claimed.

Release URL: https://github.com/anushannga/UF-Dehemi/releases/tag/v2.430 (verify publication before posting).

All Linux, Windows and macOS jobs passed in [run 38226501752](https://github.com/anushannga/UF-Dehemi/actions/runs/38226501752), testing `574efaca4d82c4ab0604663d703ad9c01e3f9c3f`. Canonical TTF hashes from all three platforms match the current release. Windows Uniscribe and actual macOS CoreText each pass 790 coverage cases per style; CoreText also passes three expected conjunct cases per style with no missing/fallback glyphs and mark-geometry checks. Linux Chromium 153.0.8010.12 passes the conditional soft-hyphen line-breaking proof in both styles. Reports: `qa/platform-validation-2.430.json`, `qa/coretext-validation-2.430.json`, `qa/browser-validation-2.430.json` and `qa/platforms/`.

Latest Fontspector links: [JSON](https://github.com/anushannga/UF-Dehemi/blob/main/qa/fontspector-2.430.json) and [HTML](https://github.com/anushannga/UF-Dehemi/blob/main/qa/fontspector-2.430.html), available after publication of this commit.

A concrete [serving coverage proposal](SUBSET-COVERAGE-PROPOSAL.md) and adjacent patch are prepared for curator review. The 17 displayed unreachable codepoints and eight additional encoded entries require upstream policy; no hosted fix is claimed.
