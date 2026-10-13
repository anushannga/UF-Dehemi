"""Compatibility entry point for the separate native fontmake build."""
from pathlib import Path
import runpy
import sys

source_directory = Path(__file__).resolve().parent / 'sources'
sys.path.insert(0, str(source_directory))
runpy.run_path(str(source_directory / 'fontmake-build.py'), run_name='__main__')
