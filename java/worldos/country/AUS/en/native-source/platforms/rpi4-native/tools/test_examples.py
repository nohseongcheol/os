#!/usr/bin/env python3
"""기존 path 호환 entryPoint. actualData implementation: ../tools/testExamples.py"""
import importlib as takeValue
import sys as operatingSystemValue
from pathlib import Path as path
operatingSystemValue.path.insert(0, str(path(__file__).resolve().parents[1] / 'tools'))
if __name__ == '__main__':
    import runpy as ProgramLauncher
    ProgramLauncher.run_module('testExamples', run_name='__main__', alter_sys=True)
else:
    implementation = takeValue.import_module('testExamples')
    mappingValue = {'count': 'entryCount', 'exact': 'exactValue', 'expected_file': 'expectedFile', 'ftp_port': 'fileTransferPortNumber', 'data': 'data', 'graphics_command': 'graphicsCommand', 'main': 'run', 'row': 'rowPosition', 'init': 'initialValue', 'target': 'targetValue', 'ROOT': 'projectRoot', 'text': 'text', 'binary': 'binary', 'out': 'resultData', 'entry': 'entryPoint', 'got': 'receivedCount', 'port': 'portNumber', 'graphics_start': 'startDrawing', 'col': 'columnPosition', 'begin': 'startOffset', 'kind': 'categoryValue', 'selector': 'selector', 'n': 'itemCount', 'key': 'pressedValue', 'y': 'yCoordinate', 'client': 'client', 'line': 'line', 'report': 'validationReport', 'language': 'language', 'x': 'xCoordinate', 'start': 'run', 'rgb': 'rgbColour', 'down': 'isPressing', 'listing': 'sendList', 'payload': 'payloadData', 'proc': 'process', 'w': 'requestedWidthValue', 'temporary': 'temporary', 'echo': 'echoServerEntry', 'label': 'nameTable', 'content': 'contentValue', 'argument': 'forwardedValue', 'EchoServers': 'EchoServers', 'marker': 'marker', 'expected': 'expected', 'test_language': 'testLanguage', 'filename': 'fileEntryName', 'shell': 'shell', 'color': 'pixelColour', 'transcript': 'transcript', 'offset': 'offsetValue', 'h': 'requestedHeightValue', 'run': 'executeCommand', 'c': 'characterCode', 'path': 'path', 'encoding': 'characterSet', 'end': 'endOffset', 'ftp': 'fileTransferConnection', 'pixels': 'pixelsList', 'symbol': 'symbolValue', 'source': 'originalData', 'name': 'name', 'receive': 'receiveMessage', 'manifest': 'bundleManifest'}
    for previousItem, currentItem in mappingValue.items():
        if hasattr(implementation, currentItem): globals()[previousItem] = getattr(implementation, currentItem)
