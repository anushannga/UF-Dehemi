# Add Dehemi — draft for the existing submission

Preparation only for [google/fonts#11099](https://github.com/google/fonts/issues/11099). The published release remains **2.440**. The unreleased **2.441 candidate** corrects embedded OFL metadata and repository build/documentation. Local QA is recorded below; candidate cross-platform CI is not yet verified. Review the personal confirmations before updating the existing issue.

**Font Project Git Repo URL:**

https://github.com/anushannga/UF-Dehemi

**Super short description of the Font Family:**

Dehemi is a Maname-derived Sinhala display family in Regular and Italic, with Latin support, licensed under SIL OFL 1.1. Original Italic artwork/hinting is retained; Regular is its unhinted upright companion. Upstream attribution and [source-history limits](https://github.com/anushannga/UF-Dehemi/blob/main/documentation/SOURCE-HISTORY.md) are disclosed. OpenAI Codex assisted with technical adjustments, source/build preparation and QA.

**Requirements:**

The checklist maps the [official template](https://github.com/google/fonts/blob/main/.github/ISSUE_TEMPLATE/1_add-font.md) with shortened wording. Personal confirmations remain unchecked. Verified repository facts include source/build availability, the selected Dehemi menu name, upstream attribution and AI disclosure.

- [ ] The entire offered project is publicly available under OFL.
- [ ] No larger retail, plus or pro version exists elsewhere.
- [ ] Source/build inputs are available, with reverse-export and acquisition limits disclosed.
- [ ] Every relevant author's work is covered by OFL; AI use is clearly disclosed.
- [ ] Upstream Reserved Font Names are absent from the family name or an exception is agreed.
- [ ] Family-name uniqueness is verified using [FontData namecheck](https://namecheck.fontdata.com/).
- [ ] The definitive app-menu family name is **Dehemi**, with Regular and Italic styles.
- [ ] The candidate supports the required Google Fonts Latin Core glyphset.
- [ ] The completed repository follows the preferred upstream structure.
- [ ] I personally read, agree to and comply with all contributing requirements.
- [ ] I will maintain the repository and participate in onboarding.

**Image:**

![Published Dehemi 2.440 Regular and Italic specimen](https://raw.githubusercontent.com/anushannga/UF-Dehemi/main/documentation/Preview.png)

**Review status:**

Local 2.441 candidate: Fontspector 1.9.0 Google Fonts profile, both fonts plus OFL, reports **213 PASS, 8 WARN, 0 FAIL**, with all four required licensing results passing. `qa/fontspector-2.441.json` and `qa/audit-context-2.441.json` record the unpublished candidate audit. Six outline/design and two inferred serving warnings remain. Only head/name tables differ from published 2.440; drawing, hinting, layout and metrics are identical. Candidate cross-platform CI is not yet verified.

The published [2.440 audit](https://github.com/anushannga/UF-Dehemi/blob/main/qa/fontspector-2.440.json) remains baseline evidence and omitted the OFL collection input; its PASS total is not directly comparable. [Warning/design evidence](https://github.com/anushannga/UF-Dehemi/blob/main/documentation/WARNING-REVIEW.md) retains the original version labels.

The final-head `cla/google` check on nam-files PR #32 succeeded; all-holder coverage for this font submission is still unconfirmed. PR #32 was closed unmerged; serving-subset work belongs to Google Fonts onboarding maintainers. No acceptance or Google Docs availability is claimed.
