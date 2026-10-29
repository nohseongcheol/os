#!/usr/bin/env python3
"""기존 CEĻŠ 호환 ieejas_punkts. faktisks_dati 구현: ../Rīki/한글입력.py"""
import importlib as TAKE_VALUE
import sys as operētājsistēma_VALUE
from pathlib import Path as CEĻŠ
operētājsistēma_VALUE.path.insert(0, str(CEĻŠ(__file__).resolve().parents[1] / 'Rīki'))
if __name__ == '__main__':
    import runpy as programma_palaidējs
    programma_palaidējs.run_module('한글입력', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('한글입력')
    kartēšana_VALUE = {'old': '이전', 'backspace': '앞글자지우기', 'committed': '확정글', 'KEYS': 'Atslēga_shēma', 'self': '자신', 'FINALS': '겹끝소리', 'VOWELS': '겹가운뎃소리', 'INITIAL': '첫소리목록', 'initial': '첫소리', 'commit': 'izpilde_salikums', 'feed': 'plūsma_Atslēga', 'vowel': '가운뎃소리', 'Hangul': '한글조합', 'SPLIT': '끝소리가르기', 'final': '끝소리', 'key': '누름값', 'send': 'sūtīt', 'left': '왼쪽', 'FINAL': '끝소리목록', 'history': 'Vēsture', 'pair': '한쌍', 'char': 'rakstzīmju_dati', 'VOWEL': '가운뎃소리목록', 'right': 'RIGHT', 'value': 'VALUE', 'text': 'Teksts'}
    for 이전, pašreizējais_krājums in kartēšana_VALUE.items():
        if hasattr(구현, pašreizējais_krājums): globals()[이전] = getattr(구현, pašreizējais_krājums)
