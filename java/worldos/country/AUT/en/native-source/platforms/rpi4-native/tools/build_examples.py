#!/usr/bin/env python3
"""기존 path 호환 entryPoint. actualData implementation: ../tools/buildExamples.py"""
import importlib as takeValue
import sys as operatingSystemValue
from pathlib import Path as path
operatingSystemValue.path.insert(0, str(path(__file__).resolve().parents[1] / 'tools'))
if __name__ == '__main__':
    import runpy as ProgramLauncher
    ProgramLauncher.run_module('buildExamples', run_name='__main__', alter_sys=True)
else:
    implementation = takeValue.import_module('buildExamples')
    mappingValue = {'out': 'resultData', 'build_examples': 'createExamples', 'files': 'fileList', 'java': 'executeJava', 'run': 'executeCommand', 'path': 'path', 'p': 'dataPosition', 'readme': 'readme', 'build_java_library': 'createJavaLibrary', 'code': 'instructionSequence', 'index': 'lookupIndex', 'classes': 'classPath', 'repo': 'repositoryPath', 'root': 'rootAddress', 'content': 'contentValue', 'source': 'originalData', 'name': 'name', 'target': 'targetValue', 'manifest': 'bundleManifest', 'language': 'language'}
    for previousItem, currentItem in mappingValue.items():
        if hasattr(implementation, currentItem): globals()[previousItem] = getattr(implementation, currentItem)
