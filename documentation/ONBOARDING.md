# Dehemi: remaining Google Fonts onboarding steps

The current family is Dehemi 2.420, with Regular and Italic styles under SIL OFL 1.1. Continue the existing [submission #11099](https://github.com/google/fonts/issues/11099). A successful build or audit does not constitute Google Fonts acceptance.

## Contributor agreements

The appropriate human contributor or authorized organization representative must complete Google's Contributor License Agreement. No agreement has been signed or legal declaration made on their behalf.

1. Sign in to [Google's CLA service](https://cla.developers.google.com/) with the contributor's own account.
2. Review and complete the Individual CLA, or the appropriate Corporate CLA if an organization owns the contribution.
3. Associate GitHub username `anushannga` with the agreement as directed by the service.
4. Confirm the contributor's coverage with the Google Fonts curators. Keep legal account information out of the public repository.

The fonts contain Maname-derived artwork and layout. Retain the upstream notice and review relevant copyright holders and contributor coverage with the curators. OFL licensing alone does not establish that Google's CLA process is complete, and this release does not claim sole ownership of the upstream work. [Official CLA explanation](https://cla.developers.google.com/about).

## Family name

The author has selected **Dehemi**, replacing `UF Dehemi`. The earlier abbreviation and hyphen are absent from the current font family name. The previous naming-exception request is no longer needed. Confirm this change in the existing submission thread; the repository can retain its historical URL.

## Technical and design review

The confirmed 2.420 Fontspector result is 196 PASS, 27 WARN, 0 FAIL, 137 SKIP and 13 INFO across both styles. Keep the current JSON/HTML reports with the submission. Historical 2.400 and 2.410 reports must be identified by version. Remaining warnings require review rather than disabling checks or assuming intentional texture resolves them. Use [WARNING-REVIEW.md](WARNING-REVIEW.md) as a review checklist and remeasure any baseline values against the current fonts.

The canonical build preserves the existing italic outlines and hinting from TTX while compiling editable native FEA. The UFO/fontmake target also compiles feature source; it does not copy binary layout tables. SFD/UFO outlines and the initial FEA originated as reverse exports, which remains part of the documented source history. The unhinted fontmake output is separately checked for shaping parity and does not replace the canonical release.

GitHub Actions defines Linux, Windows and macOS jobs; the current three-platform run is pending. Local Windows Uniscribe validation has passed 789 cases per style. Verify the actual CI run for the submission commit and retain its reports before claiming CI success or a CoreText result. Local HarfBuzz/FreeType checks alone do not establish a macOS native result, and Uniscribe parity does not certify DirectWrite or every Windows application. Human review should also cover the Regular design, textured contours, mark placement, line spacing, browser and office use, and print/export behavior.

## Submission update and Google Docs

Update the existing issue with the new family name, release/source links, exact confirmed audit results, platform results and the remaining contributor/design review items. Avoid opening a duplicate issue. The [submission draft](SUBMISSION-DRAFT.md) is a preparation document until its placeholders are verified and the update is posted.

Public OFL distribution and Google Fonts onboarding are separate steps. Neither a public release nor local QA guarantees Google Docs availability. Curator acceptance and any downstream product availability remain external decisions. [Official onboarding guide](https://googlefonts.github.io/gf-guide/onboarding.html).
