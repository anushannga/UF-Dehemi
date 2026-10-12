# Remaining warning investigation, 2026-10-12

Production remains Dehemi 2.440: **207 PASS, 8 WARN, 0 FAIL** with the unmodified Fontspector 1.9.0 Google Fonts profile. None of the experimental fonts was released or installed. These experiments did not eliminate the eight warnings safely.

Three isolated candidates were tested:

| Candidate | PASS | WARN | FAIL | Outcome |
| --- | ---: | ---: | ---: | --- |
| PathOps Boolean normalization, replacement unhinted outlines | 203 | 9 | 1 | Outline warnings persist; sole FAIL is the temporary directory family name. |
| Morphological closing at 3 design units, quadratic conversion | 202 | 13 | 0 | More warnings and changed ink texture; rejected. |
| FontForge removeOverlap/simplify/correctDirection/autoHint/autoInstr | 192 | 21 | 6 | More outline warnings and lost/changed metadata; rejected. |

The original hinted Italic cannot safely retain point-indexed hint programs after arbitrary contour reordering. Replacement hinting in the FontForge trial did not produce a better audit. Experimental checks retain their raw results; tests were not disabled to obtain a smaller count.

All 81 encoded glyphs flagged by contour_count now have current-release, 112-pixel Regular/Italic proofs: [page 1](review-2.440/contour-atlas-1.png), [page 2](review-2.440/contour-atlas-2.png), [page 3](review-2.440/contour-atlas-3.png), [page 4](review-2.440/contour-atlas-4.png), [page 5](review-2.440/contour-atlas-5.png). The five pages were visually inspected for legibility and labels. Visible ink cuts explain some disconnected contours; this is evidence for design review, not certification of every segment or curator approval. Exact font hashes are in [the atlas record](../qa/contour-review-atlas-2.440.json).

The serving coverage proposal is now submitted as [googlefonts/nam-files draft PR 32](https://github.com/googlefonts/nam-files/pull/32). It proposes 18 additions with regenerated data. Its overlap test is **not green**: the baseline has 15 conflicting codepoints, and the proposal has 22, including seven new cross-subset conflicts. Tests and exceptions were not altered. Maintainers must decide the shared-character policy; this is not ready to merge, does not resolve the eight additional aliases/controls/PUA entries, and has not changed Google's serving system.

Next required work is targeted hint-aware outline/design review and upstream serving policy review. There is no new font binary, release, warning-zero claim, or Google acceptance claim in this update.
