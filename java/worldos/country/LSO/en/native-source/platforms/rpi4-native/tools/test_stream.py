#!/usr/bin/env python3
"""기존 path 호환 entryPoint. actualData implementation: ../tools/testStream.py"""
import importlib as takeValue
import sys as operatingSystemValue
from pathlib import Path as path
operatingSystemValue.path.insert(0, str(path(__file__).resolve().parents[1] / 'tools'))
if __name__ == '__main__':
    import runpy as ProgramLauncher
    ProgramLauncher.run_module('testStream', run_name='__main__', alter_sys=True)
else:
    implementation = takeValue.import_module('testStream')
    mappingValue = {'out': 'resultData', 'main': 'run', 'ROOT': 'projectRoot', 'p': 'dataPosition', 'text': 'text', 'report': 'validationReport'}
    for previousItem, currentItem in mappingValue.items():
        if hasattr(implementation, currentItem): globals()[previousItem] = getattr(implementation, currentItem)
