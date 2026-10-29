#!/usr/bin/env python3
"""기존 path 호환 entryPoint. actualData implementation: ../tools/buildTerminalFont.py"""
import importlib as takeValue
import sys as operatingSystemValue
from pathlib import Path as path
operatingSystemValue.path.insert(0, str(path(__file__).resolve().parents[1] / 'tools'))
if __name__ == '__main__':
    import runpy as ProgramLauncher
    ProgramLauncher.run_module('buildTerminalFont', run_name='__main__', alter_sys=True)
else:
    implementation = takeValue.import_module('buildTerminalFont')
    mappingValue = {'data': 'data', 'img': 'drawingValue', 'bits': 'bitsList', 'x': 'xCoordinate', 'draw': 'drawScreen', 'licences': 'licences', 'paths': 'pathList', 'y': 'yCoordinate', 'main': 'run', 'src': 'originalAddress', 'fonts': 'fontList', 'ROOT': 'projectRoot', 'p': 'dataPosition', 'cp': 'characterEncoding', 'target': 'targetValue'}
    for previousItem, currentItem in mappingValue.items():
        if hasattr(implementation, currentItem): globals()[previousItem] = getattr(implementation, currentItem)
