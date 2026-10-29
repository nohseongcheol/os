#!/usr/bin/env python3
"""기존 path 호환 entryPoint. actualData implementation: ../tools/testHangulInput.py"""
import importlib as takeValue
import sys as operatingSystemValue
from pathlib import Path as path
operatingSystemValue.path.insert(0, str(path(__file__).resolve().parents[1] / 'tools'))
if __name__ == '__main__':
    import runpy as ProgramLauncher
    ProgramLauncher.run_module('testHangulInput', run_name='__main__', alter_sys=True)
else:
    implementation = takeValue.import_module('testHangulInput')
    mappingValue = {'expected': 'expected', 'Keyboard': 'Keyboard', 'press': 'pressKey', 'self': 'selfValue', 'test_modes_repeat_and_commit': 'testModesRepeatAndCommit', 'keys': 'pressedKeys', 'test_paste_and_unicode': 'testPasteAndUnicode', 'data': 'data', 'key': 'pressedValue', 'send': 'send', 'test_words': 'testWords', 'InputTests': 'testHangulInput', 'test_backspace': 'testBackspace', 'symbol': 'symbolValue', 'char': 'characterData', 'type': 'typeCategory'}
    for previousItem, currentItem in mappingValue.items():
        if hasattr(implementation, currentItem): globals()[previousItem] = getattr(implementation, currentItem)
