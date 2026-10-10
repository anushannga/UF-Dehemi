# UF-Dehemi

Sinhala Unicode italic font, version 2.351, distributed under SIL Open Font License 1.1. The family name is **UF-Dehemi**. This preparation snapshot preserves the Tight-232 artwork, outlines, metrics, layout and hinting of the current release. It does not change the installed font.

## Contents

- `fonts/ttf/UF-Dehemi-Italic.ttf`: current release binary.
- `OFL.txt`: license and attribution.
- `sources/`: editable reverse exports and historical design/build materials.
- `qa/`: Fontspector 1.9.0 Google Fonts profile results and prior release validation.
- `documentation/Preview.png`: specimen of the current design.

## Audit status — not ready for Google Fonts submission

Fontspector reports **91 PASS, 23 WARN, 5 FAIL, 84 SKIP and 6 INFO**. Counts are report severity totals; skipped checks are not passes. The Google Fonts glyph coverage check passes. Sinhala U+0D81 is missing. Existing contour, overlap and language shaping warnings still need review; see the complete HTML/JSON reports.

Blocking failures:

1. Google Fonts family naming rules reject the hyphen and abbreviation in `UF-Dehemi`. The requested name has been retained. A Google Fonts-specific name requires a separate design/branding decision.
2. The family contains only Italic; the checker requires a Roman counterpart. A real upright design needs author review. Relabeling the italic as Regular would misrepresent it.
3. U+02C9 spacing macron has zero advance width.
4. Static RIBBI naming has redundant name IDs 16 and 17.

Additional onboarding work: all required contributor agreements, review of upstream rights/attribution, reproducible production build, and curator acceptance. This is a public development snapshot for an initial submission and naming exception discussion, not an approved Google Fonts release. No completed CLA or acceptance is claimed. Publication in Google Fonts does not guarantee availability in Google Docs.

## Source and ownership record

This release derives from Maname, including outlines and shaping data. Its upstream copyright attribution remains in OFL.txt. The historical V12 generator transforms Maname outlines; the glyph-path JSON is associated with that workflow. These materials must not be described as wholly independent drawings or exclusive ownership evidence. ANUSHANGA K P is the release preparer's supplied name; it is not independently verified legal certification.

The SFD/UFO files are editable exports of the TTF, not proof of an original source workflow. Their successful export does not establish fontmake rebuild parity. Historical scripts reference local inputs and need conversion into a portable build before submission. Keep the TTF as the authoritative release until rebuild comparison has passed.

AI tooling (OpenAI Codex) assisted with release metadata, source exports, audit documentation, packaging and submission preparation. The historical V12 workflow transforms upstream Maname artwork; no claim is made that AI-assisted packaging establishes independent ownership of those outlines.

## Recheck

Use Fontspector 1.9.0 or a documented later version:

```sh
fontspector -p googlefonts --json qa/fontspector.json --html qa/fontspector.html fonts/ttf/UF-Dehemi-Italic.ttf
```

Official requirements: https://googlefonts.github.io/gf-guide/requirements.html

Official onboarding: https://googlefonts.github.io/gf-guide/onboarding.html

Fontspector: https://github.com/fonttools/fontspector

OFL permissions and conditions are in OFL.txt. Font software may be used, modified and redistributed under that license; the font cannot be sold by itself.
