#!/usr/bin/env python3
"""기존 path 호환 entryPoint. actualData implementation: ../tools/desktopView.py"""
import importlib as takeValue
import sys as operatingSystemValue
from pathlib import Path as path
operatingSystemValue.path.insert(0, str(path(__file__).resolve().parents[1] / 'tools'))
if __name__ == '__main__':
    import runpy as ProgramLauncher
    ProgramLauncher.run_module('desktopView', run_name='__main__', alter_sys=True)
else:
    implementation = takeValue.import_module('desktopView')
    mappingValue = {'count': 'entryCount', 'special': 'specialKey', 'error': 'error', 'exact': 'exactValue', 'network': 'network', 'closed': 'isClosed', 'length': 'lengthValue', 'opened': 'opened', 'ftp_port': 'fileTransferPortNumber', 'server': 'serverValue', 'resources': 'resources', 'data': 'data', 'shift': 'shiftKey', 'send': 'send', 'run_desktop': 'runDesktop', 'protocol': 'NetworkABI', 'forwards': 'forwardingRules', 'host': 'Host', 'text': 'text', 'korean': 'korean', 'port': 'portNumber', 'signum': 'signalNumber', 'version': 'versionNumber', 'parser': 'parser', 'bridge': 'bridge', 'kind': 'categoryValue', 'tail': 'endingPart', 'size': 'size', 'previous_buttons': 'previousButtons', 'key': 'pressedValue', 'y': 'yCoordinate', 'prefix': 'leadingPart', 'client': 'client', 'char': 'characterData', 'work': 'workingPath', 'Keyboard': 'Keyboard', 'x': 'xCoordinate', 'down': 'isPressing', 'net': 'networkBridgeEntry', 'self': 'selfValue', 'mode_changed': 'modeChanged', 'serial': 'serialIo', 'args': 'argumentArray', 'Hangul': 'composeHangul', 'chunk': 'fragmentValue', 'proc': 'process', 'Desktop': 'connectDesktop', 'buttons': 'buttons', 'thread': 'worker', 'pressed': 'isPressed', 'previous': 'previous', 'toggle': 'switchMode', 'command': 'command', 'sock': 'socketValue', 'frame': 'executionFrame', 'ctrl': 'controlKey', 'path': 'path', 'cp': 'characterEncoding', 'terminate': 'terminate', 'security': 'security', 'vnc_port': 'vncPort', 'body': 'bodyText', 'index': 'lookupIndex', 'exited': 'hasExited', 'keysym': 'keySymbol', 'output': 'output', 'keyboard': 'keyboardEntry', 'interrupted': 'interrupted', 'listener': 'receivePort', 'reader': 'reader', 'NetworkBridge': 'networkBridge', 'gui': 'drawingScreen', 'worker': 'processingTask'}
    for previousItem, currentItem in mappingValue.items():
        if hasattr(implementation, currentItem): globals()[previousItem] = getattr(implementation, currentItem)
