#!/usr/bin/env python3
"""기존 path 호환 entryPoint. actualData implementation: ../tools/executeCommand.py"""
import importlib as takeValue
import sys as operatingSystemValue
from pathlib import Path as path
operatingSystemValue.path.insert(0, str(path(__file__).resolve().parents[1] / 'tools'))
if __name__ == '__main__':
    import runpy as ProgramLauncher
    ProgramLauncher.run_module('executeCommand', run_name='__main__', alter_sys=True)
else:
    implementation = takeValue.import_module('executeCommand')
    mappingValue = {'supported': 'supportedFeatures', 'parser': 'parser', 'qemu': 'MockMachine', 'run_desktop': 'runDesktop', 'main': 'run', 'host': 'Host', 'status': 'stateValue', 'NetworkBridge': 'networkBridge', 'ROOT': 'projectRoot', 'bridge': 'bridge', 'loader': 'loader', 'base': 'backgroundValue', 'options': 'options', 'binary': 'binary', 'args': 'argumentArray', 'command': 'command'}
    for previousItem, currentItem in mappingValue.items():
        if hasattr(implementation, currentItem): globals()[previousItem] = getattr(implementation, currentItem)
