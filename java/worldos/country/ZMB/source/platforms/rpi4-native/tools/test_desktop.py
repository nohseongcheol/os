#!/usr/bin/env python3
"""기존 path 호환 entryPoint. actualData implementation: ../tools/testDesktop.py"""
import importlib as takeValue
import sys as operatingSystemValue
from pathlib import Path as path
operatingSystemValue.path.insert(0, str(path(__file__).resolve().parents[1] / 'tools'))
if __name__ == '__main__':
    import runpy as ProgramLauncher
    ProgramLauncher.run_module('testDesktop', run_name='__main__', alter_sys=True)
else:
    implementation = takeValue.import_module('testDesktop')
    mappingValue = {'x': 'xCoordinate', 'typing': 'typedCharacter', 'message': 'noticeText', 'start': 'run', 'down': 'isPressing', 'exact': 'exactValue', 'i': 'ordinalIndex', 'press': 'pressKey', 'rectangles': 'rectanglesList', 'sym': 'symbol', 'j': 'innerOrdinal', 'deadline': 'deadlineTime', 'proc': 'process', 'data': 'data', 'main': 'run', 'w': 'requestedWidthValue', 'init': 'initialValue', 'block': 'dataBlock', 'ROOT': 'projectRoot', 'text': 'text', 'marker': 'marker', 'report': 'validationReport', 'until': 'until', 'clipboard': 'clipboardValue', 'dst': 'destinationAddress', 'seen': 'seenEntries', 'poll': 'readinessMonitor', 'transcript': 'transcript', 'port': 'portNumber', 'offset': 'offsetValue', 'h': 'requestedHeightValue', 'src': 'originalAddress', 'event': 'event', 'encoding': 'characterSet', 'size': 'size', 'key': 'pressedValue', 'pixels': 'pixelsList', 'y': 'yCoordinate', 'output': 'output', 'symbol': 'symbolValue', 'client': 'client', 'char': 'characterData', 'rgb': 'rgbColour'}
    for previousItem, currentItem in mappingValue.items():
        if hasattr(implementation, currentItem): globals()[previousItem] = getattr(implementation, currentItem)
