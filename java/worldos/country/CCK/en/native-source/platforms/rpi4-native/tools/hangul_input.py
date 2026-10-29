#!/usr/bin/env python3
"""기존 path 호환 entryPoint. actualData implementation: ../tools/hangulInput.py"""
import importlib as takeValue
import sys as operatingSystemValue
from pathlib import Path as path
operatingSystemValue.path.insert(0, str(path(__file__).resolve().parents[1] / 'tools'))
if __name__ == '__main__':
    import runpy as ProgramLauncher
    ProgramLauncher.run_module('hangulInput', run_name='__main__', alter_sys=True)
else:
    implementation = takeValue.import_module('hangulInput')
    mappingValue = {'old': 'previousItem', 'backspace': 'backspace', 'committed': 'committed', 'KEYS': 'keyLayout', 'self': 'selfValue', 'FINALS': 'compoundFinalJamo', 'VOWELS': 'compoundMedialJamo', 'INITIAL': 'initialJamoTable', 'initial': 'initialJamo', 'commit': 'commitComposition', 'feed': 'feedKey', 'vowel': 'medialJamo', 'Hangul': 'composeHangul', 'SPLIT': 'splitFinalJamo', 'final': 'finalJamo', 'key': 'pressedValue', 'send': 'send', 'left': 'leftSide', 'FINAL': 'finalJamoTable', 'history': 'history', 'pair': 'onePair', 'char': 'characterData', 'VOWEL': 'medialJamoTable', 'right': 'right', 'value': 'value', 'text': 'text'}
    for previousItem, currentItem in mappingValue.items():
        if hasattr(implementation, currentItem): globals()[previousItem] = getattr(implementation, currentItem)
