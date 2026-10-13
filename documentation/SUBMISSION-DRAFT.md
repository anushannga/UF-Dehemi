# Add Dehemi — draft for the existing submission

Preparation only for [google/fonts#11099](https://github.com/google/fonts/issues/11099). The published release remains **2.440**. The unreleased **2.441 candidate** corrects embedded OFL metadata and repository build/documentation. Recorded three-platform CI passes. Review the [verification evidence](CHECKLIST-VERIFICATION.md) and remaining confirmations before updating the existing issue.

**Font Project Git Repo URL:**

https://github.com/anushannga/UF-Dehemi

**Super short description of the Font Family:**

Dehemi is a Maname-derived Sinhala display family in Regular and Italic, with Latin support, licensed under SIL OFL 1.1. Original Italic artwork/hinting is retained; Regular is its unhinted upright companion. Upstream attribution and [source-history limits](https://github.com/anushannga/UF-Dehemi/blob/main/documentation/SOURCE-HISTORY.md) are disclosed. OpenAI Codex assisted with technical adjustments, source/build preparation and QA.

**Requirements:**

The checklist maps the [official template](https://github.com/google/fonts/blob/main/.github/ISSUE_TEMPLATE/1_add-font.md) with shortened wording. Ten items have recorded evidence or author confirmation. The complete earlier author-rights chain remains unconfirmed; known upstream OFL and AI disclosure do not independently certify that chain.

- [x] The current two-style project is publicly available under OFL, and the author agrees to OFL.
- [x] The author confirms the identified old restricted edition is no longer sold or offered; no active larger retail/pro offering was identified.
- [x] Source/build inputs are available, with reverse-export and acquisition limits disclosed.
- [ ] Every relevant author's work is covered by OFL; AI use is clearly disclosed.
- [x] No RFN declaration was found in the inspected current and Maname license headers.
- [x] [FontData namecheck](https://namecheck.fontdata.com/?q=Dehemi) found no exact-name match on 13 October 2026.
- [x] The definitive app-menu family name is **Dehemi**, with Regular and Italic styles.
- [x] Both candidate styles support all 319 required Latin Core Unicode codepoints.
- [x] The listed preferred upstream repository structure elements are present.
- [x] The author confirms personally reading and agreeing to follow the contributing requirements.
- [x] The author agrees to maintenance and community participation during onboarding.

**Image:**

![Published Dehemi 2.440 Regular and Italic specimen](https://raw.githubusercontent.com/anushannga/UF-Dehemi/main/documentation/Preview.png)

**Review status:**

Candidate Fontspector 1.9.0 Google Fonts profile, both fonts plus OFL: **213 PASS, 8 WARN, 0 FAIL**, with all four required licensing results passing. `qa/fontspector-2.441.json` and `qa/audit-context-2.441.json` record the unreleased candidate audit. Six outline/design and two inferred serving warnings remain. Only head/name tables differ from published 2.440; drawing, hinting, layout and metrics are identical. [Linux, Windows and macOS CI](https://github.com/anushannga/UF-Dehemi/actions/runs/38353650647) passes at `23d68dde8facfc8cd7187e07ee5d9abd5fb64b1f`.

The published [2.440 audit](https://github.com/anushannga/UF-Dehemi/blob/main/qa/fontspector-2.440.json) remains baseline evidence and omitted the OFL collection input; its PASS total is not directly comparable. [Warning/design evidence](https://github.com/anushannga/UF-Dehemi/blob/main/documentation/WARNING-REVIEW.md) retains the original version labels.

The final-head `cla/google` check on nam-files PR #32 succeeded; all-holder coverage for this font submission is still unconfirmed. PR #32 was closed unmerged; serving-subset work belongs to Google Fonts onboarding maintainers. No acceptance or Google Docs availability is claimed.
