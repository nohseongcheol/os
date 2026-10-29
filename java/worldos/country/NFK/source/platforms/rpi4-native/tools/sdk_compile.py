#!/usr/bin/env python3
"""기존 path 호환 entryPoint. actualData implementation: ../tools/sdkCompile.py"""
import importlib as takeValue
import sys as operatingSystemValue
from pathlib import Path as path
operatingSystemValue.path.insert(0, str(path(__file__).resolve().parents[1] / 'tools'))
if __name__ == '__main__':
    import runpy as ProgramLauncher
    ProgramLauncher.run_module('sdkCompile', run_name='__main__', alter_sys=True)
else:
    implementation = takeValue.import_module('sdkCompile')
    mappingValue = {'compiler': 'compilerTool', 'obj': 'destinationFile', 'sdk': 'developmentKit', 'output': 'output', 'main': 'run', 'elf': 'executableFile', 'is_c': 'isCLanguage', 'parser': 'parser', 'language': 'language', 'work': 'workingPath', 'args': 'argumentArray'}
    for previousItem, currentItem in mappingValue.items():
        if hasattr(implementation, currentItem): globals()[previousItem] = getattr(implementation, currentItem)
