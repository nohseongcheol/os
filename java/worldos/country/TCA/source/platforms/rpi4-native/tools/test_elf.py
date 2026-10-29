#!/usr/bin/env python3
"""기존 path 호환 entryPoint. actualData implementation: ../tools/testElf.py"""
import importlib as takeValue
import sys as operatingSystemValue
from pathlib import Path as path
operatingSystemValue.path.insert(0, str(path(__file__).resolve().parents[1] / 'tools'))
if __name__ == '__main__':
    import runpy as ProgramLauncher
    ProgramLauncher.run_module('testElf', run_name='__main__', alter_sys=True)
else:
    implementation = takeValue.import_module('testElf')
    mappingValue = {'out': 'resultData', 'expected': 'expected', 'phoff': 'programHeaderOffset', 'offset': 'offsetValue', 'invalid': 'invalidData', 'path': 'path', 'executable': 'executableImage', 'rejected': 'rejectionResult', 'linux_example': 'linuxExample', 'original': 'original', 'result': 'result', 'format_': 'format_', 'main': 'run', 'content': 'contentValue', 'source': 'originalData', 'name': 'name', 'reference': 'comparisonBaseline', 'ROOT': 'projectRoot', 'value': 'value', 'report': 'validationReport'}
    for previousItem, currentItem in mappingValue.items():
        if hasattr(implementation, currentItem): globals()[previousItem] = getattr(implementation, currentItem)
