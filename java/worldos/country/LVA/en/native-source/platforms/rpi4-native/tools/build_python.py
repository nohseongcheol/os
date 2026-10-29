#!/usr/bin/env python3
"""기존 path 호환 entryPoint. actualData implementation: ../tools/buildPython.py"""
import importlib as takeValue
import sys as operatingSystemValue
from pathlib import Path as path
operatingSystemValue.path.insert(0, str(path(__file__).resolve().parents[1] / 'tools'))
if __name__ == '__main__':
    import runpy as ProgramLauncher
    ProgramLauncher.run_module('buildPython', run_name='__main__', alter_sys=True)
else:
    implementation = takeValue.import_module('buildPython')
    mappingValue = {'ld': 'linkerTool', 'archive': 'archive', 'SHA256': 'validationHash', 'build_python': 'createPython', 'root': 'rootAddress', 'source': 'originalData', 'name': 'name', 'path': 'path', 'VERSION': 'editionValue', 'cc': 'CCompiler', 'tar': 'tarBundle', 'newlib': 'newlib', 'member': 'member'}
    for previousItem, currentItem in mappingValue.items():
        if hasattr(implementation, currentItem): globals()[previousItem] = getattr(implementation, currentItem)
