# Dehemi onboarding readiness

Published release: **2.440**. The unreleased **2.441 candidate** corrects embedded OFL metadata and repository build/documentation. Local full-profile QA reports **213 PASS, 8 WARN, 0 FAIL, 133 SKIP, 15 INFO**, with the OFL file supplied explicitly and all four required licensing results passing. [Audit context](../qa/audit-context-2.441.json). New cross-platform candidate CI is not yet verified. Continue [google/fonts#11099](https://github.com/google/fonts/issues/11099), rather than opening a duplicate submission.

The author should personally read the [Google Fonts Guide](https://googlefonts.github.io/gf-guide/) and review the [official Add Font template](https://github.com/google/fonts/blob/main/.github/ISSUE_TEMPLATE/1_add-font.md), as [requested by the maintainer](https://github.com/google/fonts/issues/11099#issuecomment-6137696893). The prepared [submission draft](SUBMISSION-DRAFT.md) keeps personal declarations unchecked. Repository repairs and automated checks cannot supply those declarations.

## Author confirmations

The following cover the official template's requirements, shortened for this checklist. An unchecked item is not a conclusion that the requirement fails.

- [ ] Confirm the public repository contains the entire offered font project under OFL.
- [ ] Confirm no larger retail, plus or pro version exists elsewhere.
- [ ] Confirm maintained source/build inputs are available in the repository.
- [ ] Confirm all relevant authors' contributions are covered by OFL and disclose AI assistance.
- [ ] Confirm known upstream Reserved Font Names are absent from Dehemi's family name, or agree an exception with Google Fonts.
- [ ] Verify family-name uniqueness using [FontData namecheck](https://namecheck.fontdata.com/).
- [ ] Confirm **Dehemi** as the definitive app-menu family name, with Regular and Italic styles.
- [ ] Confirm candidate coverage of the required [Google Fonts Latin Core](https://github.com/googlefonts/glyphsets/blob/main/data/results/txt/nice-names/GF_Latin_Core.txt).
- [ ] Confirm the completed repository meets the [preferred upstream structure](https://googlefonts.github.io/gf-guide/upstream.html), including the one-command build and specimen.
- [ ] Personally read, agree to and comply with the full contributing requirements.
- [ ] Personally commit to repository maintenance and participation during onboarding.

Verified repository facts: maintained source/build inputs are present; reverse-export and acquisition limits are disclosed in [SOURCE-HISTORY.md](SOURCE-HISTORY.md). Current app-menu naming is Dehemi. AI assistance and upstream Maname attribution are disclosed. Current Dehemi and inspected Maname license notices contain no RFN declaration. These facts do not fill the author's personal confirmations.

## Contributor agreement evidence

The `cla/google` check for `bf52e4d` on [nam-files PR #32](https://github.com/googlefonts/nam-files/pull/32/checks) succeeded on 12 October 2026, after the initial failed bot invocation. The earlier bot comment is not the current check result.

That check concerns the subset PR's contributor. It does not independently confirm coverage of all Maname/Dehemi copyright holders for a font submission. The appropriate human contributor or representative should verify coverage with curators using [Google's CLA service](https://cla.developers.google.com/). No agreement or legal declaration is made on anyone's behalf here.

## Design and serving review

The published 2.440 audit has eight raw warnings: six outline/design messages and two inferred serving-coverage messages. Preserve raw reports and [warning evidence](WARNING-REVIEW.md). Human review should cover the upright companion, ink cuts, mark attachment, line spacing, real text and export behavior. Point-indexed Italic hinting limits arbitrary contour reordering; unsuccessful cleanup experiments remain [documented](OUTLINE-INVESTIGATION-2.440.md).

[nam-files PR #32](https://github.com/googlefonts/nam-files/pull/32) is closed and unmerged. Simon Cozens explained that distributing bases and marks across separate served fonts can [break attachment](https://github.com/googlefonts/nam-files/pull/32#issuecomment-6129761200), and [directed serving work to the onboarding team](https://github.com/googlefonts/nam-files/pull/32#issuecomment-6137450860). The local [proposal and patch](SUBSET-COVERAGE-PROPOSAL.md) remain historical evidence, not an active merge request or deployed fix.

The candidate's [table comparison](../qa/metadata-change-2.441.json) proves drawing, hinting, layout and metric table bytes unchanged from 2.440. Local canonical, Windows and native fontmake checks pass, as linked from the README. Candidate cross-platform CI remains to be verified. The historical 2.440 audit omitted the OFL collection input, so its PASS total must not be treated as directly comparable with the candidate's complete audit. Tests cover a recorded corpus, with no every-application, Office/PDF or DirectWrite certification. Acceptance and downstream Google Docs availability are external decisions.
