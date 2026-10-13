#!/usr/bin/env bash
set -euo pipefail

# Install requirements.txt first. DEHEMI_PYTHON may select a Python executable;
# provide one executable name or path, without arguments. It is never evaluated
# as shell code. Python 3.12 is the documented build environment.
python_executable="${DEHEMI_PYTHON:-python}"
source_directory="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
project_directory="$(CDPATH= cd -- "$source_directory/.." && pwd)"

if ! command -v -- "$python_executable" >/dev/null 2>&1; then
    printf 'Python executable not found: %s\n' "$python_executable" >&2
    exit 127
fi

cd -- "$project_directory"

# Canonical TTX build, followed by the separate UFO/fontmake development build
# and its shaping comparisons. This wrapper does not migrate the release source
# or resolve the provenance limits documented in documentation/SOURCE-HISTORY.md.
"$python_executable" sources/build.py
"$python_executable" sources/fontmake-build.py
