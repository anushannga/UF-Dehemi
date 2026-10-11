# UF Dehemi

Sinhala Unicode display family, version 2.400, SIL Open Font License 1.1. Regular and Italic. App-menu family name: **UF Dehemi**.

Italic preserves the original Tight-232 outlines, hinting and Sinhala layout. Regular is a mechanically upright companion from those outlines, with old hinting removed after transformation; human design and platform review remain necessary.

## Release and QA

Release fonts are in `fonts/ttf/ufdehemi/`.

Fixed: hyphen in family name, duplicate name IDs 16/17, zero-width U+02C9 spacing macron, missing Roman companion and missing U+0D81 chandrabindu. The new ring-and-dot chandrabindu is based on existing artwork. U+0D81 is not the letter ඇ (U+0D87). All assigned Sinhala-block codepoints are mapped.

Fontspector 1.9.0: **175 PASS, 46 WARN, 2 FAIL, 143 SKIP, 9 INFO** across both styles. Both FAILs are the UF abbreviation, once per style. Naming exception remains requested. Existing contour, language shaping, layout classification and metric warnings remain for review. Full reports: `qa/fontspector-2.400.html` and `.json`. No all-pass or acceptance claim is made.

788 HarfBuzz shaping cases and 5,435 FreeType renders pass per style. Original italic coordinates and prior Sinhala shaping outputs are preserved. These tests do not certify visual correctness for every string or universal platform support.

## Build

```sh
pip install -r requirements.txt
python build.py
python validate.py
python fontmake-build.py
```

Canonical release: fontTools builds from `sources/Upstream-Tight232.ttx` and `build.py`, retaining upstream layout and italic hinting. Editable SFD/UFO files are reverse exports, not the original design workflow.

The fontmake development target compiles UFO outlines and overlays canonical layout/name tables. FontForge's reverse-export FEA is incompatible with feaLib; it is omitted from this development compilation. This target does not replace the release fonts. A native editable feature workflow and complete source-to-release parity remain migration work. GitHub Actions runs both build targets and regression checks.

## Attribution and onboarding

Derived from Maname; see `OFL.txt` for upstream attribution and SIL OFL 1.1. Historical V12 scripts transform Maname outlines. No exclusive or wholly independent ownership is claimed. ANUSHANGA K P is the supplied release preparer name; Pasan Anushanga appears in historical modification attribution.

OpenAI Codex assisted with metadata, technical adjustments, upright transformation, source exports, automation, QA, documentation and submission.

Outstanding: contributor agreements, upstream contributor review, curator design review, naming exception and warning review. Submission: https://github.com/google/fonts/issues/11099 . This is not an approved Google Fonts or Google Docs font.

Official guide: https://googlefonts.github.io/gf-guide/onboarding.html
