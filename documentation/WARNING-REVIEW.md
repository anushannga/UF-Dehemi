# Dehemi: remaining warning review

This document records design and shaping questions that require review after the
technical corrections. A warning is not automatically a malformed font, and it
must not be converted to a pass by disabling the check. The current Fontspector
JSON/HTML report is the authority for the checks and counts in the release being
reviewed. This document does not claim that every check passes or that Google
Fonts has accepted the family.

The original Tight-232 italic artwork has an ink texture. Some outlines contain
small cuts, additional contours and irregular edges. The Regular companion was
created by mechanically removing the italic shear and requires its own design
review. Blanket outline cleanup could visibly change the font that the designer
asked to preserve. Where a warning involves artwork, keep the original as a
comparison and review a proposed correction before adopting it.

## Review checklist

| Check | Current review status and proposed verification |
| --- | --- |
| `outline_jaggy_segments` | **Open: visual review.** The detector reports acute changes between line and curve segments. Some may be intentional cuts in the ink texture; others may be unintended spikes. Inspect each reported segment at high magnification, then compare normal-size specimens at 12, 24, 48 and 96 px. Correct unintended spikes locally. Do not smooth every edge, because that would remove the original texture. Compare corrected glyphs and common Sinhala words in both styles. |
| `contour_count` | **Open: mapping and artwork review.** The check compares contour counts with reference fonts. Texture and disconnected ink details can make the correct design exceed those counts. Check each reported glyph against its Unicode assignment and the intended letter, including the distinction between U+0D87 ඇ and U+0D81 chandrabindu. Confirm there are no accidental duplicate contours, missing counters or wrongly mapped letters. Retain intentional details and document the reviewed exceptions. |
| `outline_direction` | **Open: fill and winding review.** Many outlines have outer contours in the direction flagged by the checker. Inspect outer contours and counters together, including nested contours and overlaps. Compare rendering with nonzero fill rules in FreeType, Windows DirectWrite and CoreText. Reversing every contour, or selectively reversing without understanding holes, can change filled areas. Normalize only with a reviewed contour hierarchy and before/after render comparison. |
| `overlapping_path_segments` | **Open: segment review.** The report includes zero-length segments and repeated path segments. Check reported segments in glyphs such as `sinTVa`, `sinTTha` and `sinTTh.virama` separately from deliberate overlapping texture. Remove proven redundant or degenerate segments locally and compare raster output. A blanket remove-overlap operation can merge contours, change small cuts and disturb the artwork. |
| `outline_semi_vertical` | **Open: Regular review.** Mechanically removing the shear and rounding to integer coordinates produces nearly horizontal or vertical lines. Inspect each reported line to distinguish rounding artifacts from intentional edge irregularity. Snap only strokes intended to be straight and compare both the isolated glyph and shaped text. Do not apply axis snapping to the original italic style. |
| `googlefonts/vertical_metrics` | **Open: line spacing and clipping review.** The 2.400 baseline uses UPM 1000, hhea ascender 1194 and descender -359, a total of 1553 (1.553 times UPM), above the check's recommended 1.2–1.5 range. Baseline actual glyph bounds are -319 to 1154. These numbers describe that baseline, and must be remeasured after glyph additions. Reducing metrics merely to meet the recommendation changes line spacing and may clip tall marks. Test all current bounds, stacked marks, multiline Sinhala/Latin text, browser line heights and print output before adjusting. Keep the family metrics consistent. |
| `opentype/GDEF_spacing_marks` | **Open: `sinVirama` shaping review.** The original virama is in GDEF mark class 3 but has advance width 237. The check questions that spacing. Do not zero its advance blindly: isolated virama and existing Sinhala substitutions may rely on the current behavior. Review its GSUB/GPOS treatment and compare standalone virama, dead consonants, ZWJ/ZWNJ forms and conjuncts, including ශ්‍රී, ක්‍රියා, ප්‍රශ්න, විද්‍යාව, න්‍යාය and ක්ෂේත්‍ර. Compare glyph advances, mark positions and appearance in multiple shaping engines before changing the width or GDEF class. New chandrabindu attachment must be tested separately. |
| `soft_hyphen` | **Open: text behavior decision.** U+00AD is present. Verify it stays invisible within an unbroken word and behaves appropriately when an application uses it for a line break. Compare browser, office and PDF output. Removing its cmap entry solely to silence a warning can reduce text compatibility; retaining it needs documented review rather than a hidden test exception. |
| `alt_caron` | **Open: Latin visual review.** The checker cannot automatically assess the decomposed `Lcaron`, `dcaron`, `lcaron` and `tcaron` outlines. Check that the accent has the intended short vertical/apostrophe-like design, appropriate placement and spacing. Review their normal-size text alongside the unaccented letters. A manual check is required; a decomposed outline alone does not establish a design error. |
| `googlefonts/glyphsets/shape_languages` | **Open: auxiliary Latin support review.** The baseline report includes missing auxiliary Latin characters and a Lithuanian `l` + combining tilde attachment warning. Re-run this check after coverage or feature changes, inspect every remaining missing character, and test any newly added composites and anchors. Basic Latin coverage passing does not establish complete support for every language listed in metadata. |
| `googlefonts/metadata/unreachable_subsetting` | **Open: served coverage review.** The baseline metadata leaves some encoded characters outside its declared subsets. Review the exact codepoints in the latest report and the intended Google Fonts subset definitions. Do not add unrelated writing-system subsets merely to silence this warning. The full local TTF can contain characters that a hosted subset does not serve; curator agreement or appropriate glyphset changes may still be needed. |

Safe metadata changes, new glyphs and newly authored feature code must be evaluated
in the latest report. Their removal from the baseline warnings does not resolve
the artwork questions above. If a technical fix introduces a new warning, record
and investigate it before publishing the next release.

## Tests and their limits

Automated build, font parsing, Unicode coverage, shaping regression and raster
tests can confirm that the tested files build and that the tested inputs produce
the expected glyphs and positions. A comparison with the earlier italic release
can detect unintended changes to existing artwork and layout. New glyphs,
new anchors and the upright companion need additional expected results and visual
review; simply matching an old result cannot establish their correctness.

For cross-platform review, record the font version, application, operating system,
shaping engine and specimen text. Test Windows DirectWrite in a browser and an
office application, macOS CoreText, and a HarfBuzz-based Linux/browser stack.
Check small and large text, multiline line spacing, combining marks, Sinhala
conjuncts, Latin accents, fallback behavior, text selection and exported PDFs.
The published test report should distinguish actual platform runs from proposed
tests; a FreeType/HarfBuzz run does not count as a DirectWrite or CoreText run.

Passing the available tests does not certify every Unicode sequence, application,
printing pipeline or future software version. Tests also do not grant Google
Fonts acceptance, place a font in Google Docs, resolve trademark/naming decisions,
or establish copyright ownership. The family was renamed to Dehemi with the
designer's approval; no `UF` family-name exception is requested for this release.

## Licensing and contributor agreements

Keep the SIL OFL 1.1 text and the Maname-derived source attribution with the fonts
and editable sources. Technical adjustments and successful builds do not remove
upstream authors' rights or make the artwork exclusively owned by the release
preparer.

Google's Contributor License Agreement must be completed by the appropriate
human contributor or authorized organization representative. An automated tool
cannot sign it, attest to a person's authority, or mark it completed without
evidence. Identify relevant contributors and copyright holders, review the source
history and the applicable contribution process, and retain confirmation of the
actual agreement. Until that review and the curator's review are complete, record
their status as pending rather than approved.
