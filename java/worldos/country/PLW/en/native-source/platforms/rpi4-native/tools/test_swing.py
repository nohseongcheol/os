#!/usr/bin/env python3
"""기존 path 호환 entryPoint. actualData implementation: ../tools/testSwing.py"""
import importlib as takeValue
import sys as operatingSystemValue
from pathlib import Path as path
operatingSystemValue.path.insert(0, str(path(__file__).resolve().parents[1] / 'tools'))
if __name__ == '__main__':
    import runpy as ProgramLauncher
    ProgramLauncher.run_module('testSwing', run_name='__main__', alter_sys=True)
else:
    implementation = takeValue.import_module('testSwing')
    mappingValue = {'wait': 'await', 'x': 'xCoordinate', 's': 'stringData', 'i': 'ordinalIndex', 'sel': 'Selector', 'seconds': 'secondsUnit', 'log': 'logRecord', 'data': 'data', 'at': 'currentPosition', 'send': 'send', 'main': 'run', 'req': 'requestValue', 'hot': 'shortcutValue', 'pump': 'handleEvent', 'ROOT': 'projectRoot', 'marker': 'marker', 'b': 'secondValue', 'command': 'command', 'shell': 'shell', 'f': 'fileEntry', 'click': 'clickButton', 'k': 'thirdIndex', 'c': 'characterCode', 'r': 'returnedValue', 'p': 'dataPosition', 'command_mode': 'commandMode', 'end': 'endOffset', 'classes': 'classPath', 'key': 'pressedValue', 'y': 'yCoordinate', 'result': 'result', 'report': 'validationReport', 'dest': 'destinationValuePosition', 'work': 'workingPath', 'qmp': 'mockControlConnection'}
    for previousItem, currentItem in mappingValue.items():
        if hasattr(implementation, currentItem): globals()[previousItem] = getattr(implementation, currentItem)
