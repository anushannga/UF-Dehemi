# Dehemi 2.440: published warning baseline

The published release remains 2.440. The unreleased 2.441 candidate corrects embedded license metadata and repository build/documentation. Its full-profile audit with both TTFs and OFL reports **213 PASS, 8 WARN, 0 FAIL, 133 SKIP, 15 INFO**, including all four required licensing results passing. [Inputs](../qa/audit-context-2.441.json), [raw report](../qa/fontspector-2.441.json). The eight warning categories persist; drawing, hinting, layout and metric table bytes are identical to 2.440. [Comparison](../qa/metadata-change-2.441.json). The historical results and proofs below retain their 2.440 labels.

Additional experiments and all 81 encoded contour-warning proofs are recorded in [the 2026-10-12 investigation](OUTLINE-INVESTIGATION-2.440.md). Production has eight raw warnings; experimental candidates were rejected. The separate serving proposal was closed unmerged, as recorded below.

Fontspector 1.9.0, unmodified Google Fonts profile, both styles: **207 PASS, 8 WARN, 0 FAIL, 137 SKIP, 15 INFO**. The 2.430 baseline had 19 WARN. No check is excluded and no raw severity is relabeled.

That historical 2.440 audit did not explicitly include OFL in the collection inputs. Its PASS total is not directly comparable with the complete 2.441 audit and must not be represented as a count of corrected font defects.

## Corrections in published 2.440

- **Eight alternate-caron warnings resolved.** Lcaron/dcaron/lcaron/tcaron now retain their actual distinctive accents and bodies as independently editable components. No punctuation or triangular combining-caron substitution is used. Expanded point order and original parent hint instructions are identical. This corrects source structure and permits the checker to inspect the component identities.
- **Two soft-hyphen warnings resolved.** Following the check's recommendation, U+00AD is not encoded: discretionary line breaking belongs to the application. An actual U+2010 hyphen reuses the original discretionary-dash drawing, without deleting any visible letter. Application browser tests exercise wide/invisible and narrow/visible conditional hyphens. Raw/default-ignorable-preserving glyph APIs may return .notdef for U+00AD; that compatibility limit is disclosed rather than represented as an every-API pass.
- **Regular overlapping-path warning resolved.** A tiny out-and-back quadratic nib in sinTI was removed from the unhinted Regular source. The real area change is 1.333 square design units. Bounds and advance remain identical. Pixels are identical through 96 px; at 144/400 px only two/three edge pixels differ. Original hinted Italic is untouched.

All 5,540 old Regular glyph renders at 12/16/24/48/96 px are identical to 2.430. All old Italic expanded coordinates and hint programs are identical; four Latin carons have 20 small antialias differences, at most 5/255, with identical bounds and advances. All other old Italic renders, including Sinhala, are identical. See [actual design regression](../qa/design-regression-2.440.json).

## Remaining eight raw messages

| Check | Messages | Review and reason retained |
| --- | ---: | --- |
| contour_count | 2 | Textured/disconnected contours differ from typical reference counts. Coverage assertions and representative mappings pass. A reference contour count is not an artistic requirement; all reported contours have not been individually certified. |
| outline_jaggy_segments | 2 | The original ink cuts include acute joins. Wholesale smoothing changes the requested artwork. Representative proofs exist; further local design changes need specialist/author review. |
| overlapping_path_segments | 1 | Original hinted Italic includes redundant/retraced points. Removing/reindexing them requires hint-aware changes or replacement hinting; the preserved original programs address those points. The unhinted Regular issue is corrected. |
| outline_direction | 1 | Original hinted Italic winding remains. Blind point reversal with old instructions risks incorrect hinting. Regular is normalized; preserved Italic is tested in available engines. |
| googlefonts/metadata/unreachable_subsetting | 2 | Inferred serving coverage is retained in the raw audit. Google Fonts maintainers handle serving subsets during onboarding. PR #32 was closed unmerged because dividing bases and marks among served fonts can break attachment; its patch is historical evidence. Full downloadable TTF coverage is distinct from hosted CSS/subsets. |

See the historical [2.430 manual proofs](../qa/manual-review-2.430.json), [texture specimen](texture-proof-2.430.png), [caron specimen](caron-proof-2.430.png), and archived [serving investigation](SUBSET-COVERAGE-PROPOSAL.md). Those images retain their true version labels. The 2.440 point/raster comparisons link their applicability to that release.

All Linux, Windows and macOS jobs passed in [run 38231411379](https://github.com/anushannga/UF-Dehemi/actions/runs/38231411379), at `6dc1621fc01401ffc11b6b8055a1b5f3dc6817f6`. The canonical font hashes from all platforms match the current release. Actual isolated Chromium conditional-hyphen checks pass on all three operating systems; native Windows Uniscribe and macOS CoreText checks also pass. Reports: `qa/platform-validation-2.440.json`, `qa/coretext-validation-2.440.json`, `qa/platforms/*-browser-validation-2.440.json`. Historical 2.430 platform reports do not count as a new run. The latest source builds, Latin/Sinhala regressions and unmodified raw reports remain authoritative for the recorded corpus. No every-application or acceptance claim is made.

Google's [official QA guidance](https://googlefonts.github.io/gf-guide/qa.html) distinguishes FAILs, which require fixes, from WARNs, which require human judgment and can reflect expected design decisions. Zero warnings is not an approval guarantee; curator design/source/serving and contributor review still apply.
