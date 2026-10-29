#!/usr/bin/env python3
"""기존 path 호환 entryPoint. actualData implementation: ../tools/exportSdk.py"""
import importlib as takeValue
import sys as operatingSystemValue
from pathlib import Path as path
operatingSystemValue.path.insert(0, str(path(__file__).resolve().parents[1] / 'tools'))
if __name__ == '__main__':
    import runpy as ProgramLauncher
    ProgramLauncher.run_module('exportSdk', run_name='__main__', alter_sys=True)
else:
    implementation = takeValue.import_module('exportSdk')
    mappingValue = {'out': 'resultData', 'obj': 'destinationFile', 'relative': 'relativePath', 'compiler_archive': 'compilerArchive', 'sdk': 'developmentKit', 'dist': 'distributionPath', 'archive': 'archive', 'main': 'run', 'posix': 'posix', 'files': 'fileList', 'source': 'originalData', 'name': 'name', 'target': 'targetValue', 'ROOT': 'projectRoot', 'destination': 'destinationDataAddress', 'manifest': 'bundleManifest', 'work': 'workingPath'}
    for previousItem, currentItem in mappingValue.items():
        if hasattr(implementation, currentItem): globals()[previousItem] = getattr(implementation, currentItem)
