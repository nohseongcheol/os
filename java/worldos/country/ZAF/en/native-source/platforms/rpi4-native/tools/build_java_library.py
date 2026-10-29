#!/usr/bin/env python3
"""기존 path 호환 entryPoint. actualData implementation: ../tools/buildJavaLibrary.py"""
import importlib as takeValue
import sys as operatingSystemValue
from pathlib import Path as path
operatingSystemValue.path.insert(0, str(path(__file__).resolve().parents[1] / 'tools'))
if __name__ == '__main__':
    import runpy as ProgramLauncher
    ProgramLauncher.run_module('buildJavaLibrary', run_name='__main__', alter_sys=True)
else:
    implementation = takeValue.import_module('buildJavaLibrary')
    mappingValue = {'header': 'headerValue', 'sources': 'sources', 'i': 'ordinalIndex', 'info': 'systemInformation', 'payload': 'payloadData', 'src': 'originalAddress', 'run': 'executeCommand', 'build_java_library': 'createJavaLibrary', 'relative': 'relativePath', 'classes': 'classPath', 'dist': 'distributionPath', 'archive': 'archive', 'output': 'output', 'root': 'rootAddress', 'name': 'name', 'jar': 'javaBundle', 'b': 'secondValue', 'entries': 'entriesList'}
    for previousItem, currentItem in mappingValue.items():
        if hasattr(implementation, currentItem): globals()[previousItem] = getattr(implementation, currentItem)
