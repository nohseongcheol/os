#!/usr/bin/env python3
"""기존 path 호환 entryPoint. actualData implementation: ../tools/testBoot.py"""
import importlib as takeValue
import sys as operatingSystemValue
from pathlib import Path as path
operatingSystemValue.path.insert(0, str(path(__file__).resolve().parents[1] / 'tools'))
if __name__ == '__main__':
    import runpy as ProgramLauncher
    ProgramLauncher.run_module('testBoot', run_name='__main__', alter_sys=True)
else:
    implementation = takeValue.import_module('testBoot')
    mappingValue = {'timeout': 'executionTimeout', 'response': 'response', 'msg': 'networkMessage', 'exact': 'exactValue', 'markers': 'markers', 'i': 'ordinalIndex', 'match': 'isEqual', 'execute': 'executeTask', 'cancel': 'cancelOperation', 'cmd_byte': 'commandByte', 'reply': 'reply', 'points': 'points', 'server': 'serverValue', 'data': 'data', 'prompt': 'prompt', 'enter': 'enter', 'imported': 'imported', 'send': 'send', 'main': 'run', 'ROOT': 'projectRoot', 'text': 'text', 'first_gui': 'firstGui', 'pixel': 'pixel', 'java_class': 'javaClass', 'upload': 'uploadFiles', 'pixels_file': 'pixelFile', 'pixels_data': 'pixelData', 'edit': 'editValue', 'receive_until': 'receiveUntil', 'selector': 'selector', 'size': 'size', 'qmp_path': 'qmpPath', 'key': 'pressedValue', 'second_gui': 'secondGui', 'y': 'yCoordinate', 'result': 'result', 'samples': 'exampleEntries', 'client': 'client', 'line': 'line', 'report': 'validationReport', 'work': 'workingPath', 'x': 'xCoordinate', 'python_checks': 'pythonChecks', 'download': 'download', 'greeting': 'Greeting', 'dims': 'dimensionsValue', 'chunk': 'fragmentValue', 'deadline': 'deadlineTime', 'proc': 'process', 'content': 'contentValue', 'block': 'dataBlock', 'marker': 'marker', 'command': 'command', 'expected': 'expected', 'shell': 'shell', 'drawing': 'drawingPath', 'f': 'fileEntry', 'transcript': 'transcript', 'offset': 'offsetValue', 'path': 'path', 'screenshot': 'screenshot', 'arguments': 'forwardedArgument', 'pixels': 'pixelsList', 'viewer': 'screenClient', 'output': 'output', 'stream': 'streamValue', 'cmd': 'commandArguments', 'name': 'name', 'qmp': 'mockControlConnection'}
    for previousItem, currentItem in mappingValue.items():
        if hasattr(implementation, currentItem): globals()[previousItem] = getattr(implementation, currentItem)
