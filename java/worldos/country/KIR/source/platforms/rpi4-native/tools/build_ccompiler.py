#!/usr/bin/env python3
"""기존 path 호환 entryPoint. actualData implementation: ../tools/buildCCompiler.py"""
import importlib as takeValue
import sys as operatingSystemValue
from pathlib import Path as path
operatingSystemValue.path.insert(0, str(path(__file__).resolve().parents[1] / 'tools'))
if __name__ == '__main__':
    import runpy as ProgramLauncher
    ProgramLauncher.run_module('buildCCompiler', run_name='__main__', alter_sys=True)
else:
    implementation = takeValue.import_module('buildCCompiler')
    mappingValue = {'out': 'resultData', 'builtins': 'builtins', 'header': 'headerValue', 'sdk': 'developmentKit', 'build_ccompiler': 'createCCompiler', 'i': 'ordinalIndex', 'elf': 'executableFile', 'run': 'executeCommand', 'flags': 'configurationBits', 'path': 'path', 'p': 'dataPosition', 'cc': 'CCompiler', 'obj': 'destinationFile', 'flag': 'settingsValue', 'ld': 'linkerTool', 'objects': 'destinationFiles', 'repo': 'repositoryPath', 'v': 'temporaryData', 'upstream': 'upstream', 'root': 'rootAddress', 'assets': 'assets', 'source': 'originalData', 'name': 'name', 'includes': 'includes'}
    for previousItem, currentItem in mappingValue.items():
        if hasattr(implementation, currentItem): globals()[previousItem] = getattr(implementation, currentItem)
