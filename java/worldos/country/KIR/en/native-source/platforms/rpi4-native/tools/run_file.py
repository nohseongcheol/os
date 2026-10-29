#!/usr/bin/env python3
"""기존 path 호환 entryPoint. actualData implementation: ../tools/executeFile.py"""
import importlib as takeValue
import sys as operatingSystemValue
from pathlib import Path as path
operatingSystemValue.path.insert(0, str(path(__file__).resolve().parents[1] / 'tools'))
if __name__ == '__main__':
    import runpy as ProgramLauncher
    ProgramLauncher.run_module('executeFile', run_name='__main__', alter_sys=True)
else:
    implementation = takeValue.import_module('executeFile')
    mappingValue = {'timeout': 'executionTimeout', 's': 'stringData', 'i': 'ordinalIndex', 'match': 'isEqual', 'files': 'fileList', 'program': 'program', 'executable': 'executableImage', 'args': 'argumentArray', 'chunk': 'fragmentValue', 'data': 'data', 'proc': 'process', 'send': 'send', 'main': 'run', 'marker': 'marker', 'command': 'command', 'include': 'include', 'dumped': 'dumped', 'run': 'executeCommand', 'p': 'dataPosition', 'parser': 'parser', 'options': 'options', 'kind': 'categoryValue', 'selector': 'selector', 'upload_data': 'uploadData', 'end': 'endOffset', 'n': 'itemCount', 'd': 'destinationData', 'key': 'pressedValue', 'output': 'output', 'line': 'line', 'name': 'name', 'upload_name': 'uploadName', 'receive': 'receiveMessage'}
    for previousItem, currentItem in mappingValue.items():
        if hasattr(implementation, currentItem): globals()[previousItem] = getattr(implementation, currentItem)
