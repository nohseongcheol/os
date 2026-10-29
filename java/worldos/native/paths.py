"""Locate optional generator inputs without a fixed developer home directory."""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def jkoros_root():
    if os.environ.get('JKOROS_ROOT'):
        return Path(os.environ['JKOROS_ROOT']).expanduser().resolve()
    for parent in (ROOT.parent, ROOT.parent.parent):
        candidate = parent / 'jkoros'
        if (candidate / 'compiler/컴파일러.py').is_file():
            return candidate
    return ROOT.parent / 'jkoros'
