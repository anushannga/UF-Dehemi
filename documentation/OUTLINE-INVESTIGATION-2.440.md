# Historical warning investigation, 2026-10-12

Production remains Dehemi 2.440: **207 PASS, 8 WARN, 0 FAIL** with the unmodified Fontspector 1.9.0 Google Fonts profile. None of the experimental fonts was released or installed. These experiments did not eliminate the eight warnings safely.

Status updated on 13 October 2026: the unreleased 2.441 candidate addresses license metadata and repository build/documentation, with a separate complete audit recorded in [WARNING-REVIEW.md](WARNING-REVIEW.md). Drawing, hinting, layout and metric table bytes are unchanged. The serving PR below is now closed unmerged; this document records the earlier experiments.

Three isolated candidates were tested:

| Candidate | PASS | WARN | FAIL | Outcome |
| --- | ---: | ---: | ---: | --- |
| PathOps Boolean normalization, replacement unhinted outlines | 203 | 9 | 1 | Outline warnings persist; sole FAIL is the temporary directory family name. |
| Morphological closing at 3 design units, quadratic conversion | 202 | 13 | 0 | More warnings and changed ink texture; rejected. |
| FontForge removeOverlap/simplify/correctDirection/autoHint/autoInstr | 192 | 21 | 6 | More outline warnings and lost/changed metadata; rejected. |

The original hinted Italic cannot safely retain point-indexed hint programs after arbitrary contour reordering. Replacement hinting in the FontForge trial did not produce a better audit. Experimental checks retain their raw results; tests were not disabled to obtain a smaller count.

All 81 encoded glyphs flagged by contour_count now have current-release, 112-pixel Regular/Italic proofs: [page 1](review-2.440/contour-atlas-1.png), [page 2](review-2.440/contour-atlas-2.png), [page 3](review-2.440/contour-atlas-3.png), [page 4](review-2.440/contour-atlas-4.png), [page 5](review-2.440/contour-atlas-5.png). The five pages were visually inspected for legibility and labels. Visible ink cuts explain some disconnected contours; this is evidence for design review, not certification of every segment or curator approval. Exact font hashes are in [the atlas record](../qa/contour-review-atlas-2.440.json).

The serving coverage proposal was submitted as [googlefonts/nam-files PR 32](https://github.com/googlefonts/nam-files/pull/32) and is now **closed, unmerged**. It proposed 18 additions with regenerated data. Its overlap test was **not green**: the baseline had 15 conflicting codepoints and the proposal had 22, including seven new cross-subset conflicts. Tests and exceptions were not altered. Simon Cozens explained the additional base/mark attachment risk across separate served fonts and directed serving-subset handling to the Google Fonts onboarding team. The retained [patch and investigation](SUBSET-COVERAGE-PROPOSAL.md) are historical evidence, not an active author-side repair request or deployed fix.

Targeted hint-aware outline/design review remains. Google Fonts maintainers handle serving during onboarding. These experiments did not produce a new release, warning-zero result or Google Fonts acceptance.
