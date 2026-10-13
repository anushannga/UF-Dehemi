# Dehemi source history

The canonical outline/hint input is `sources/Upstream-Tight232.ttx`, an XML export of the supplied UF-Dehemi Tight-232 font stage (internal version 2.330). It records that derivative font stage, rather than the original Maname drawing sources. The current build preserves existing italic outlines and glyph hint instructions while compiling maintained feature source and adding documented technical changes.

The historical `sources/build_collection_v12.py` reads `C:/Users/MCTech/Downloads/Sinhala-Fonts-main/maname.ttf`, transforms its glyph outlines and generates Sinhala design previews. It also reads a separate Many Weatz font for a reference preview. These paths describe the historical study environment and are not inputs to the current release build. A [13 October input audit](UPSTREAM-IDENTITY.md) found an exact byte match with an official Google Fonts distributed Maname TTF and records its URL and hash. Original acquisition details and byte-exact reproduction from a pinned upstream source commit remain unverified. The current reproducible build begins at the recorded Tight-232 stage; it does not reproduce every earlier acquisition and design step.

`sources/features.fea` began as a reverse export of the existing layout. It has been corrected into editable FEA compiled through fontTools feaLib. Both canonical and UFO/fontmake builds compile source features; they do not overlay GSUB/GPOS/GDEF from a compiled release font. The maintained build implementations and helpers are in `sources/`; `sources/build.sh` runs both targets, while root Python entry points remain compatibility wrappers. The SFD and UFO outline sources are also reverse exports. The unhinted fontmake development output differs from the canonical font in outline/hint representation and is tested separately for shaping parity. See [the build workflow and its limits](../README.md#build) and [the review checklist](WARNING-REVIEW.md).

## Recorded source hashes

SHA-256 of the current repository source content, with LF line endings. A checkout using CRLF can have a different byte hash without changing the parsed source:

| Source | SHA-256 |
| --- | --- |
| `sources/Upstream-Tight232.ttx` | `308ed5954a1f95a627e43f165721bca71a2d6d7be8d804282041b11c876cca57` |
| `sources/features.fea` | `a9dc1d77c73453515afb448696277d0ce3f3d1f449d41308484ba38e76af49f3` |

These hashes identify the recorded files, not the missing upstream acquisition history. Recompute them when either source changes.

## Upstream attribution

The [historical replay](HISTORICAL-REPLAY.md) now reconstructs all recorded
Maname-derived glyph geometry, metrics, cmap/layout and final hint programs, with
matching canonical TTX fingerprints. This closes the technical composition gap;
the original acquisition date and original command log are still not certified.

The retained Maname notice matches the upstream [OFL.txt](https://github.com/mooniak/maname-font/blob/main/OFL.txt): Copyright 2015-2023 The Maname Project Authors. Its header contains no Reserved Font Name declaration. The full SIL OFL 1.1 terms and upstream copyright remain in this project's license and fonts.

Upstream [AUTHORS.txt](https://github.com/mooniak/maname-font/blob/main/AUTHORS.txt) identifies Pathum Egodawatta for copyright purposes. [CONTRIBUTORS.txt](https://github.com/mooniak/maname-font/blob/main/CONTRIBUTORS.txt) is empty in the inspected upstream repository. An empty contributor file does not establish complete contributor coverage or a completed Google CLA. [The upstream README](https://github.com/mooniak/maname-font) describes the project's design history.

This record does not certify exclusive ownership or an original drawing date. The final-head CLA check on the separate subset PR succeeded, while all-holder coverage for this font submission remains unconfirmed. See [ONBOARDING.md](ONBOARDING.md) for the evidence and remaining human confirmations.
