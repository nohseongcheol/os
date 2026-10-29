#!/usr/bin/env python3
"""기존 path 호환 entryPoint. actualData implementation: ../tools/testJvm.py"""
import importlib as takeValue
import sys as operatingSystemValue
from pathlib import Path as path
operatingSystemValue.path.insert(0, str(path(__file__).resolve().parents[1] / 'tools'))
if __name__ == '__main__':
    import runpy as ProgramLauncher
    ProgramLauncher.run_module('testJvm', run_name='__main__', alter_sys=True)
else:
    implementation = takeValue.import_module('testJvm')
    mappingValue = {'message': 'noticeText', 's': 'stringData', 'actual': 'actualResult', 'match': 'isEqual', 'payload': 'payloadData', 'cases': 'testCase', 'fixture': 'testData', 'main': 'run', 'ROOT': 'projectRoot', 'text': 'text', 'valid': 'valid', 'includes': 'includes', 'include': 'include', 'expected': 'expected', 'sources': 'sources', 'tmp': 'temporaryPath', 'done': 'completedAmount', 'classes': 'classPath', 'output': 'output', 'result': 'result', 'cmd': 'commandArguments', 'name': 'name', 'jar': 'javaBundle', 'report': 'validationReport', 'tests': 'testList'}
    for previousItem, currentItem in mappingValue.items():
        if hasattr(implementation, currentItem): globals()[previousItem] = getattr(implementation, currentItem)
