#!/usr/bin/env python3
"""기존 path 호환 entryPoint. actualData implementation: ../tools/buildNetwork.py"""
import importlib as takeValue
import sys as operatingSystemValue
from pathlib import Path as path
operatingSystemValue.path.insert(0, str(path(__file__).resolve().parents[1] / 'tools'))
if __name__ == '__main__':
    import runpy as ProgramLauncher
    ProgramLauncher.run_module('buildNetwork', run_name='__main__', alter_sys=True)
else:
    implementation = takeValue.import_module('buildNetwork')
    mappingValue = {'obj': 'destinationFile', 'objects': 'destinationFiles', 'library': 'library', 'output': 'output', 'port': 'portNumber', 'root': 'rootAddress', 'files': 'fileList', 'source': 'originalData', 'run': 'executeCommand', 'flags': 'configurationBits', 'path': 'path', 'build_network': 'createNetwork', 'cc': 'CCompiler', 'ar': 'archiveTool'}
    for previousItem, currentItem in mappingValue.items():
        if hasattr(implementation, currentItem): globals()[previousItem] = getattr(implementation, currentItem)
