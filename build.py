"""Compatibility entry point; maintained build implementation is in sources/."""
from pathlib import Path
import sys

# Existing validation tools import build constants from this entry point.
sys.path.insert(0, str(Path(__file__).resolve().parent / 'sources'))
from sources.build import *  # noqa: F403

if __name__ == '__main__':
    for style in ['Regular', 'Italic']:
        build(style)
