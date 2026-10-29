#!/usr/bin/env python3
"""기존 path 호환 entryPoint. actualData implementation: ../tools/buildUserSpace.py"""
import importlib as takeValue
import sys as operatingSystemValue
from pathlib import Path as path
operatingSystemValue.path.insert(0, str(path(__file__).resolve().parents[1] / 'tools'))
if __name__ == '__main__':
    import runpy as ProgramLauncher
    ProgramLauncher.run_module('buildUserSpace', run_name='__main__', alter_sys=True)
else:
    implementation = takeValue.import_module('buildUserSpace')
    mappingValue = {'mode': 'methodMode', 'header': 'headerValue', 'i': 'ordinalIndex', 'build_ccompiler': 'createCCompiler', 'ar': 'archiveTool', 'posix': 'posix', 'payload': 'payloadData', 'flags': 'configurationBits', 'cases': 'testCase', 'cc': 'CCompiler', 'data': 'data', 'build_java_library': 'createJavaLibrary', 'ld': 'linkerTool', 'repo': 'repositoryPath', 'build_python': 'createPython', 'inc': 'includePath', 'argument': 'forwardedValue', 'text': 'text', 'headers': 'headerList', 'cxx': 'cppCompiler', 'valid': 'valid', 'build': 'build', 'build_users': 'createUserSpace', 'compiler': 'compilerTool', 'uzlib': 'uzlib', 'extra': 'additionalRegion', 'phoff': 'programHeaderOffset', 'offset': 'offsetValue', 'text_address': 'commandAddress', 'abi': 'CallAbi', 'assembly': 'assembly', 'run': 'executeCommand', 'path': 'path', 'p': 'dataPosition', 'changed': 'changed', 'n': 'itemCount', 'flag': 'settingsValue', 'index': 'lookupIndex', 'classes': 'classPath', 'output': 'output', 'loads': 'loads', 'data_address': 'dataAddress', 'symbol': 'symbolValue', 'root': 'rootAddress', 'patches': 'modifications', 'source': 'originalData', 'sizes': 'sizes', 'blobs': 'blobs', 'name': 'name', 'value': 'value', 'fmt': 'dataFormat', 'work': 'workingPath'}
    for previousItem, currentItem in mappingValue.items():
        if hasattr(implementation, currentItem): globals()[previousItem] = getattr(implementation, currentItem)
