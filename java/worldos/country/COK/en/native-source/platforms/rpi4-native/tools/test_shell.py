#!/usr/bin/env python3
"""기존 path 호환 entryPoint. actualData implementation: ../tools/testShell.py"""
import importlib as takeValue
import sys as operatingSystemValue
from pathlib import Path as path
operatingSystemValue.path.insert(0, str(path(__file__).resolve().parents[1] / 'tools'))
if __name__ == '__main__':
    import runpy as ProgramLauncher
    ProgramLauncher.run_module('testShell', run_name='__main__', alter_sys=True)
else:
    implementation = takeValue.import_module('testShell')
    mappingValue = {'timeout': 'executionTimeout', 'x': 'xCoordinate', 'msg': 'networkMessage', 'i': 'ordinalIndex', 'reply': 'reply', 'call': 'invoke', 'args': 'argumentArray', 'chunk': 'fragmentValue', 'data': 'data', 'proc': 'process', 'long_text': 'longText', 'restored': 'restoredData', 'send': 'send', 'file': 'file', 'main': 'run', 'found': 'searchResult', 'ROOT': 'projectRoot', 'text': 'text', 'marker': 'marker', 'command': 'command', 'expected': 'expected', 'pixel': 'pixel', 'shell': 'shell', 'poll': 'readinessMonitor', 'transcript': 'transcript', 'end': 'endOffset', 'image': 'image', 'key': 'pressedValue', 'y': 'yCoordinate', 'output': 'output', 'result': 'result', 'client': 'client', 'line': 'line', 'stream': 'streamValue', 'name': 'name', 'value': 'value', 'receive': 'receiveMessage', 'report': 'validationReport', 'work': 'workingPath', 'qmp': 'mockControlConnection'}
    for previousItem, currentItem in mappingValue.items():
        if hasattr(implementation, currentItem): globals()[previousItem] = getattr(implementation, currentItem)
