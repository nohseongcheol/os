#!/usr/bin/env python3
"""기존 cesta_2 호환 vstupní_bod. skutečný_data implementace: ../nástroje/한글입력.py"""
import importlib as VZÍT_HODNOTA
import sys as operační_systém_HODNOTA
from pathlib import Path as cesta_2
operační_systém_HODNOTA.path.insert(0, str(cesta_2(__file__).resolve().parents[1] / 'nástroje'))
if __name__ == '__main__':
    import runpy as program_Launcher
    program_Launcher.run_module('한글입력', run_name='__main__', alter_sys=True)
else:
    implementace = VZÍT_HODNOTA.import_module('한글입력')
    대응 = {'old': 'Předchozí_zboží', 'backspace': '앞글자지우기', 'committed': '확정글', 'KEYS': 'Klíč_Navigace', 'self': '자신', 'FINALS': '겹끝소리', 'VOWELS': '겹가운뎃소리', 'INITIAL': '첫소리목록', 'initial': '첫소리', 'commit': 'zápis_složení', 'feed': 'novinky_Klíč', 'vowel': '가운뎃소리', 'Hangul': '한글조합', 'SPLIT': '끝소리가르기', 'final': '끝소리', 'key': '누름값', 'send': 'poslat', 'left': '왼쪽', 'FINAL': '끝소리목록', 'history': 'Historie', 'pair': '한쌍', 'char': 'textová_data', 'VOWEL': '가운뎃소리목록', 'right': 'právo', 'value': 'HODNOTA', 'text': 'text'}
    for Předchozí_zboží, dobrá_zboží in 대응.items():
        if hasattr(implementace, dobrá_zboží): globals()[Předchozí_zboží] = getattr(implementace, dobrá_zboží)
