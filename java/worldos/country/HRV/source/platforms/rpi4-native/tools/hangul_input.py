#!/usr/bin/env python3
"""기존 PUTANJA 호환 unos_p. stvaran_podaci 구현: ../Alati/한글입력.py"""
import importlib as TAKE_VALUE
import sys as operacijski_sustav_VALUE
from pathlib import Path as PUTANJA
operacijski_sustav_VALUE.path.insert(0, str(PUTANJA(__file__).resolve().parents[1] / 'Alati'))
if __name__ == '__main__':
    import runpy as program_pokretač
    program_pokretač.run_module('한글입력', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('한글입력')
    mapiranje_VALUE = {'old': '이전', 'backspace': '앞글자지우기', 'committed': '확정글', 'KEYS': 'Ključ_Raspored', 'self': '자신', 'FINALS': '겹끝소리', 'VOWELS': '겹가운뎃소리', 'INITIAL': '첫소리목록', 'initial': '첫소리', 'commit': '조합확정', 'feed': 'sažeci_Ključ', 'vowel': '가운뎃소리', 'Hangul': '한글조합', 'SPLIT': '끝소리가르기', 'final': '끝소리', 'key': '누름값', 'send': 'slati', 'left': '왼쪽', 'FINAL': '끝소리목록', 'history': 'Povijest', 'pair': '한쌍', 'char': 'znakovni_podaci', 'VOWEL': '가운뎃소리목록', 'right': 'RIGHT', 'value': 'VALUE', 'text': 'Tekst'}
    for 이전, redovno_artikl in mapiranje_VALUE.items():
        if hasattr(구현, redovno_artikl): globals()[이전] = getattr(구현, redovno_artikl)
