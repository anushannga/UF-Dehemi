# Historical source replay — 13 October 2026

A current reconstruction now accounts for the complete recorded Maname-to-
Tight232 artwork pipeline. It verifies source composition; it does not certify
exclusive authorship, original acquisition dates, the historical command log,
contributor agreements or Google Fonts acceptance.

## Recorded evidence

The committed [Maname input](../sources/history/inputs/Maname-Distributed-v2.ttf)
has SHA-256 `8e616ff912bf881ffafbf032c9b80a46d0200c6037271352871d526b3be3f24f` and
matches the official Google Fonts distributed binary documented in
[UPSTREAM-IDENTITY.md](UPSTREAM-IDENTITY.md). Its upstream OFL and copyright are
bundled unchanged. The project modifications remain under the project OFL and
Pasan/AI assistance attribution.

Six recovered scripts are preserved as [hash-pinned historical snapshots](../sources/history/script-manifest.json).
The current [replay recipe](../sources/history/replay.py) redirects their outputs
into `build/history-replay/`; it never replaces release fonts or canonical source.

| Verification | Result |
| --- | --- |
| Alphabet path source | All 59 recorded replacement paths reproduced exactly from Maname and the procedural exit code. |
| Production stage | All 1,086 glyph outlines and metrics match the recorded production font. |
| Texture and cleanup | All 1,086 outlines/metrics match each recorded Ink, Clean and Final stage. |
| Layout and repertoire | cmap and complete GSUB/GPOS/GDEF semantic XML match at every verified stage. |
| Final spacing | The reconstructed 80-unit sin* change followed by the observed seven-unit Sinhala change reproduces all Tight232 outlines and metrics. The seven-unit step affects 513 glyphs, including ten Sinhala digits. |
| Hinting | ttfautohint-py 0.6.1 defaults reproduce fpgm/prep/cvt and all 1,086 glyph programs of the Final/Tight232 fonts. The bundled executable identifies itself as ttfautohint 1.8.4.16-eb64. |
| Canonical source | Complete geometry/metrics/cmap/layout and hint fingerprints of the committed Tight232 TTX match the reconstructed target. |

[Machine-readable results](../qa/history-replay-2.441.json) and
[observed baseline fingerprints](../sources/history/baseline-fingerprints.json)
record these comparisons. Layout fingerprints use full normalized table XML:
TTX recompilation can pack offsets differently without changing the table's
meaning. Hint tables and programs are compared as exact bytes.

## Other font inputs

The alphabet replay executes only the Maname-based `lettering()` function. It
does not execute `reference()` or load Many Weatz. Production, texture, cleanup
and metrics scripts consume only Maname or the preceding reconstructed stage.
The matching complete glyph set supplies positive evidence that Many Weatz or
the separate Noto-based prototype did not supply artwork to this recorded chain.
Many Weatz reference preview artwork is not bundled here.

This is stronger evidence than relying on a README's claim that a reference font
was not copied. It establishes the source composition of the inspected artifacts,
without pretending to audit every unrelated local experiment.

## Reproduce

Use Python 3.12 in a separate environment if installing these optional historical
dependencies:

```sh
python -m pip install -r sources/history/requirements.txt
python sources/history/replay.py
```

The optional environment is separate from the normal release build. The recipe
verifies script/input hashes before replay and asserts agreement with all five
observed stages plus the committed canonical source. It writes its report under
`qa/` and all reconstructed fonts under ignored `build/`.

## Scope of the licensing conclusion

The recorded artwork/layout composition is now traceable to the identified OFL
Maname input and the documented project transformations/additions. Known upstream
credit is retained and AI assistance is disclosed. This supports the checklist's
documented source-license statement; it does not establish sole ownership of
Maname, invent a human drawing history or certify AI-generated copyright rights.

The seven-unit recipe was reconstructed today from exact artifact differences;
the original script has not been recovered. Defaults reproduce the hint bytes,
but that does not prove which command the historical operator typed. Full font
file hashes differ because metadata/packing/history differ. Those remaining
archival limits do not introduce an unidentified glyph source into the inspected
composition. Curators still decide design/source suitability and contributor
agreement coverage.
