#!/usr/bin/env python3
"""기존 path 호환 entryPoint. actualData implementation: ../tools/buildSystem.py"""
import importlib as takeValue
import sys as operatingSystemValue
from pathlib import Path as path
operatingSystemValue.path.insert(0, str(path(__file__).resolve().parents[1] / 'tools'))
if __name__ == '__main__':
    import runpy as ProgramLauncher
    ProgramLauncher.run_module('buildSystem', run_name='__main__', alter_sys=True)
else:
    implementation = takeValue.import_module('buildSystem')
    mappingValue = {'network': 'network', 'BUILD': 'buildPath', 'ar': 'archiveTool', 'build_examples': 'createExamples', 'posix': 'posix', 'font_data': 'fontData', 'flags': 'configurationBits', 'a': 'firstValue', 'cc': 'CCompiler', 'args': 'argumentArray', 'source_flags': 'originalConfiguration', 'ld': 'linkerTool', 'method': 'methodEntry', 'main': 'run', 'objcopy': 'objectFileConverter', 'ROOT': 'projectRoot', 'cxx': 'cppCompiler', 'includes': 'includes', 'compiler': 'compilerTool', 'build_users': 'createUserSpace', 'f': 'fileEntry', 'extra': 'additionalRegion', 'exports': 'exportTable', 'jobs': 'buildJobs', 'run': 'executeCommand', 'path': 'path', 'REPO': 'repositoryRoot', 'tool': 'tools', 'classes': 'classPath', 'output': 'output', 'samples': 'exampleEntries', 'symbol': 'symbolValue', 'source': 'originalData', 'name': 'name', 'build_network': 'createNetwork', 'font_info': 'fontInformation', 'manifest': 'bundleManifest', 'work': 'workingPath'}
    for previousItem, currentItem in mappingValue.items():
        if hasattr(implementation, currentItem): globals()[previousItem] = getattr(implementation, currentItem)
