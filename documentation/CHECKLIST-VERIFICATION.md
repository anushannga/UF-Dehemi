# Dehemi checklist verification — 13 October 2026

Scope: the public Dehemi repository and its unreleased 2.441 candidate in
[draft PR 1](https://github.com/anushannga/UF-Dehemi/pull/1). This verifies evidence
against the [official submission template](https://github.com/google/fonts/blob/main/.github/ISSUE_TEMPLATE/1_add-font.md).
It does not supply personal declarations the author has not made.

| Requirement | Finding | Evidence / remaining limit |
| --- | --- | --- |
| 1. Entire offered project public and OFL | Verified for the current two-style repository; author agrees to OFL | Public GitHub repository, root OFL, license bundled with both fonts, embedded licensing checks pass. Author explicitly agreed to OFL in this review. Earlier prototypes are not evidence of a larger current offering. |
| 2. No larger retail/pro version elsewhere | Historical edition identified; final current-offering declaration unconfirmed | Local Independent 3.000 files contain restricted paid-license terms. When asked current edition versus old proposal, the author replied `paranai` (old). No current larger retail offering was identified in the scoped search. This is not an explicit worldwide no-retail declaration; old files were not deleted or relicensed. |
| 3. Sources available | Verified | Both styles have committed UFO/SFD sources, TTX, maintained FEA/helpers and a one-command build in sources/. Reverse-export and historical-build limits remain disclosed. |
| 4. All relevant authors' work licensed and AI disclosed | Known Maname OFL and AI disclosure verified; complete rights chain unconfirmed | Maname OFL/copyright retained; AUTHORS/CONTRIBUTORS record known roles. README/submission disclose Codex. Missing historical pipeline details prevent certifying every earlier contribution. The separate successful CLA check does not establish every copyright holder's coverage. |
| 5. Reserved Font Names respected | Verified for inspected current and upstream notices | No RFN declaration appears in either OFL header. The generic RFN definition in the license body is not a reservation. |
| 6. Unique family name | Required database check completed; no exact match | FontData search for Dehemi returned no font by that exact name on 13 October. General web searches found no separate exact-name typeface offering. This is the prescribed limited name check, not trademark clearance. |
| 7. Definitive app-menu name | Verified | Both generated fonts use family Dehemi, styles Regular/Italic. Metadata validation confirms exact names; the former UF exception is withdrawn. |
| 8. Latin Core supported | Verified Unicode coverage in both styles | All 319 codepoints in pinned GF Latin Core map to non-.notdef glyphs. [Exact report](../qa/latin-core-2.441.json). Shaping/typography quality remains covered by separate QA and design review. |
| 9. Preferred repository structure | Verified listed structural elements | AUTHORS, CONTRIBUTORS, OFL, README/specimen, documentation, organized font output, preferred-editor sources, source build entry, requirements and ignore files are present. Native fontmake and canonical builds pass. Source-method acceptance remains a curator decision. |
| 10. Author personally read/agreed to all requirements | Not confirmed | The author's replies confirmed OFL/community maintenance and described the old prototype, but did not confirm personally reading and agreeing to the full guide. The agent's reading does not fill this item. |
| 11. Maintain and participate in onboarding | Author confirmed | The author agreed to OFL and maintenance with community participation. The repository is public and supports contributions. This is an author commitment, not an automated test result. |

## Name and coverage evidence

[FontData result](https://namecheck.fontdata.com/?q=Dehemi): the visible result
states that no font by that exact name was found. Similar-sounding suggestions
are not exact-name collisions. No registration or name-listing submission was made.

The Latin Core comparison uses the official `.nam` list at glyphsets commit
`432104e3ecb119c44b3cc29d7209d7b54bf41017`, not an inferred serving subset. Both
styles contain all 319 encoded characters with real glyph mappings. Serving
warnings are a different concern and remain with onboarding maintainers.

## Build and QA evidence

The candidate's last code revision and provenance documentation at
`23d68dde8facfc8cd7187e07ee5d9abd5fb64b1f` pass
[Linux, Windows and macOS CI](https://github.com/anushannga/UF-Dehemi/actions/runs/38353650647).
Full Fontspector 1.9.0: 213 PASS, 8 WARN, 0 FAIL, 133 SKIP, 15 INFO; all four
required licensing results pass. [Audit context](../qa/audit-context-2.441.json).
Drawing, hinting, layout and metric tables are identical to published 2.440.

Remaining outside these checklist facts: six design/outline warnings, complete
historical source reconstruction, all-holder contributor coverage, and curator
design/source acceptance. The font is Maname-derived; this verification does not
relabel it as independently drawn or promise Google Fonts/Google Docs availability.
