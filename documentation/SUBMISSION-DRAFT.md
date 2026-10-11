# Existing Google Fonts submission: Dehemi 2.420 update draft

Status: preparation draft for [google/fonts#11099](https://github.com/google/fonts/issues/11099). Verify the release and CI run links before posting this update; this file does not itself submit or approve the font.

Family: **Dehemi**

Styles: **Regular and Italic**, version **2.420**

Public source repository: https://github.com/anushannga/UF-Dehemi

Release preparer/contact: **ANUSHANGA K P**, GitHub **anushannga**. Pasan Anushanga is credited for the historical modifications; upstream Maname authors are credited in the license and fonts.

License: **SIL Open Font License 1.1**, with upstream Maname copyright retained.

## Proposed update

The author has selected the family name **Dehemi**, replacing UF Dehemi and removing the abbreviation issue. The earlier naming-exception request can be withdrawn. This is an update to the existing submission.

Version 2.420 supplies Regular and Italic, corrects macron advance width and static naming metadata, and includes chandrabindu U+0D81 with nonspacing mark attachment, the rupee sign, line/paragraph separators and updated metadata. Existing Tight-232 italic outlines and glyph hint instructions are preserved. The Regular companion removes the italic shear from both outlines and positioning anchors, and needs human design review.

The canonical build retains the TTX outline/hint source and compiles maintained native FEA. The UFO/fontmake development target compiles editable features directly and checks shaping parity; it does not overlay binary layout tables. SFD/UFO outlines and the initial FEA were reverse exports, and that source history remains documented. The development fontmake outputs are unhinted and not pixel-identical to the canonical release.

Local 2.420 validation records 788 HarfBuzz shaping cases and 5,450 FreeType glyph renders per style, with Sinhala coverage, metadata and mark-attachment assertions. Existing italic artwork and tested Sinhala shaping remain unchanged.

Fontspector 1.9.0 Google Fonts profile, both 2.420 styles: **196 PASS, 27 WARN, 0 FAIL, 137 SKIP and 13 INFO**. Reports: `qa/fontspector-2.420.json` and `qa/fontspector-2.420.html`. Remaining outline, contour, texture, language and metric warnings require review; zero failures does not imply all checks passed.

Windows Uniscribe validation passes **789 shaping cases per style**; report: `qa/windows-validation-2.420.json`. This result is separate from HarfBuzz/FreeType tests and does not certify all Windows applications or DirectWrite behavior.

Platform CI: Linux, Windows and macOS jobs are configured for the canonical build, regression checks and native fontmake build, with Windows native shaping and macOS CoreText checks. The three-platform run is pending. Add the exact release-commit run URL and actual job results after completion; no CI or macOS pass is claimed here.

Contributor agreements, upstream contributor coverage, curator design review and warning review remain pending. The Maname-derived source attribution is retained, and exclusive ownership is not claimed. Google Fonts acceptance and Google Docs availability are not claimed.

Release URL: **pending publication/verification**.

CI run URL and confirmed platform results: **pending verification**.

Latest Fontspector links: [JSON](https://github.com/anushannga/UF-Dehemi/blob/main/qa/fontspector-2.420.json) and [HTML](https://github.com/anushannga/UF-Dehemi/blob/main/qa/fontspector-2.420.html), available after publication of this commit.
