#!/usr/bin/env python3
"""기존 Putanja 호환 unos_p. stvaran_podaci 구현: ../Alati/한글입력.py"""
import importlib as TAKE_VALUE
import sys as operativni_sistem_VALUE
from pathlib import Path as Putanja
operativni_sistem_VALUE.path.insert(0, str(Putanja(__file__).resolve().parents[1] / 'Alati'))
if __name__ == '__main__':
    import runpy as program_pokretač
    program_pokretač.run_module('한글입력', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('한글입력')
    대응 = {'old': '이전', 'backspace': '앞글자지우기', 'committed': '확정글', 'KEYS': 'ključ_izgled', 'self': '자신', 'FINALS': '겹끝소리', 'VOWELS': '겹가운뎃소리', 'INITIAL': '첫소리목록', 'initial': '첫소리', 'commit': '조합확정', 'feed': 'sažetak_ključ', 'vowel': '가운뎃소리', 'Hangul': '한글조합', 'SPLIT': '끝소리가르기', 'final': '끝소리', 'key': '누름값', 'send': 'poslati', 'left': '왼쪽', 'FINAL': '끝소리목록', 'history': 'Historija', 'pair': '한쌍', 'char': 'znak_podaci', 'VOWEL': '가운뎃소리목록', 'right': 'RIGHT', 'value': 'VALUE', 'text': 'Tekst'}
    for 이전, trenutno_stavka in 대응.items():
        if hasattr(구현, trenutno_stavka): globals()[이전] = getattr(구현, trenutno_stavka)
