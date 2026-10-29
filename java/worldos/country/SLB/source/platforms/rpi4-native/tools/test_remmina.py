#!/usr/bin/env python3
"""기존 path 호환 entryPoint. actualData implementation: ../tools/testRemmina.py"""
import importlib as takeValue
import sys as operatingSystemValue
from pathlib import Path as path
operatingSystemValue.path.insert(0, str(path(__file__).resolve().parents[1] / 'tools'))
if __name__ == '__main__':
    import runpy as ProgramLauncher
    ProgramLauncher.run_module('testRemmina', run_name='__main__', alter_sys=True)
else:
    implementation = takeValue.import_module('testRemmina')
    mappingValue = {'wait': 'await', 'typing': 'typedCharacter', 'start': 'run', 'profile': 'profile', 'focused': 'focused', 'serial': 'serialIo', 'keys': 'pressedKeys', 'server': 'serverValue', 'log': 'logRecord', 'args': 'argumentArray', 'deadline': 'deadlineTime', 'data': 'data', 'candidate': 'candidate', 'logs': 'logRecords', 'kw': 'namedArgument', 'number': 'numericValue', 'main': 'run', 'ready': 'preparationComplete', 'found': 'searchResult', 'guest': 'guest', 'ROOT': 'projectRoot', 'marker': 'marker', 'text': 'text', 'out': 'resultData', 'env': 'environment', 'f': 'fileEntry', 'port': 'portNumber', 'offset': 'offsetValue', 'version': 'versionNumber', 'p': 'dataPosition', 'selector': 'selector', 'xvfb': 'virtualDisplay', 'display': 'displayDevice', 'n': 'itemCount', 'key': 'pressedValue', 'processes': 'runningProcesses', 'rootfs': 'rootfs', 'xdo': 'virtualInputTool', 'name': 'name', 'window': 'window', 'report': 'validationReport', 'work': 'workingPath'}
    for previousItem, currentItem in mappingValue.items():
        if hasattr(implementation, currentItem): globals()[previousItem] = getattr(implementation, currentItem)
