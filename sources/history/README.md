# Historical verification inputs

This is an optional current reconstruction, separate from the production build.
See [the evidence and limits](../../documentation/HISTORICAL-REPLAY.md).

- `inputs/` contains the identified Maname distributed input and its retained OFL.
- `original/` contains six recovered script snapshots, preserved without rewriting
  their historical code. Their old paths are overridden by the replay harness.
- `script-manifest.json` records LF-normalized snapshot hashes.
- `baseline-fingerprints.json` records read-only observations of five existing
  historical font stages, including exact font file hashes.
- `replay.py` verifies the snapshots, reconstructs the artwork/layout/metrics and
  hint programs, and compares against these observations and canonical TTX.

Many Weatz is not an input to the replay and its reference artwork is not shipped.
This folder does not record or invent historical execution/acquisition dates.
