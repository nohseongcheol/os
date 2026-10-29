#!/usr/bin/env python3
"""기존 path 호환 entryPoint. actualData implementation: ../tools/testWindows.py"""
import importlib as takeValue
import sys as operatingSystemValue
from pathlib import Path as path
operatingSystemValue.path.insert(0, str(path(__file__).resolve().parents[1] / 'tools'))
if __name__ == '__main__':
    import runpy as ProgramLauncher
    ProgramLauncher.run_module('testWindows', run_name='__main__', alter_sys=True)
else:
    implementation = takeValue.import_module('testWindows')
    mappingValue = {'wait': 'await', 'x': 'xCoordinate', 's': 'stringData', 'xy': 'coordinatePair', 'sel': 'Selector', 'seconds': 'secondsUnit', 'log': 'logRecord', 'at': 'currentPosition', 'send': 'send', 'main': 'run', 'req': 'requestValue', 'hot': 'shortcutValue', 'pump': 'handleEvent', 'ROOT': 'projectRoot', 'marker': 'marker', 'b': 'secondValue', 'command': 'command', 'shell': 'shell', 'f': 'fileEntry', 'color': 'pixelColour', 'click': 'clickButton', 'k': 'thirdIndex', 'c': 'characterCode', 'r': 'returnedValue', 'p': 'dataPosition', 'done': 'completedAmount', 'end': 'endOffset', 'command_mode': 'commandMode', 'key': 'pressedValue', 'y': 'yCoordinate', 'pixels': 'pixelsList', 'result': 'result', 'report': 'validationReport', 'dest': 'destinationValuePosition', 'work': 'workingPath', 'qmp': 'mockControlConnection'}
    for previousItem, currentItem in mappingValue.items():
        if hasattr(implementation, currentItem): globals()[previousItem] = getattr(implementation, currentItem)
