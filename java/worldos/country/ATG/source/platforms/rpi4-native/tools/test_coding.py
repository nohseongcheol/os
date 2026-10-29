#!/usr/bin/env python3
"""기존 path 호환 entryPoint. actualData implementation: ../tools/testCoding.py"""
import importlib as takeValue
import sys as operatingSystemValue
from pathlib import Path as path
operatingSystemValue.path.insert(0, str(path(__file__).resolve().parents[1] / 'tools'))
if __name__ == '__main__':
    import runpy as ProgramLauncher
    ProgramLauncher.run_module('testCoding', run_name='__main__', alter_sys=True)
else:
    implementation = takeValue.import_module('testCoding')
    mappingValue = {'out': 'resultData', 'expected': 'expected', 'sdk': 'developmentKit', 'suffix': 'suffixValue', 'arc': 'compressedBundle', 'main': 'run', 'elf': 'executableFile', 'run': 'executeCommand', 'name': 'name', 'path': 'path', 'p': 'dataPosition', 'ROOT': 'projectRoot', 'report': 'validationReport', 'args': 'argumentArray'}
    for previousItem, currentItem in mappingValue.items():
        if hasattr(implementation, currentItem): globals()[previousItem] = getattr(implementation, currentItem)
