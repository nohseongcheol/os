#!/usr/bin/env python3
"""기존 Cesta 호환 položka_bod. skutočný_údaje 구현: ../Nástroje/한글입력.py"""
import importlib as TAKE_VALUE
import sys as operačný_systém_VALUE
from pathlib import Path as Cesta
operačný_systém_VALUE.path.insert(0, str(Cesta(__file__).resolve().parents[1] / 'Nástroje'))
if __name__ == '__main__':
    import runpy as program_spúšťač
    program_spúšťač.run_module('한글입력', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('한글입력')
    mapovanie_VALUE = {'old': '이전', 'backspace': '앞글자지우기', 'committed': '확정글', 'KEYS': 'Kľúč_Navigácia', 'self': '자신', 'FINALS': '겹끝소리', 'VOWELS': '겹가운뎃소리', 'INITIAL': '첫소리목록', 'initial': '첫소리', 'commit': '조합확정', 'feed': 'súhrnný_obsah_Kľúč', 'vowel': '가운뎃소리', 'Hangul': '한글조합', 'SPLIT': '끝소리가르기', 'final': '끝소리', 'key': '누름값', 'send': 'odoslať', 'left': '왼쪽', 'FINAL': '끝소리목록', 'history': 'História', 'pair': '한쌍', 'char': 'znakové_údaje', 'VOWEL': '가운뎃소리목록', 'right': 'RIGHT', 'value': 'VALUE', 'text': 'Spracovanie_textu'}
    for 이전, v_termíne_splatnosti_položka in mapovanie_VALUE.items():
        if hasattr(구현, v_termíne_splatnosti_položka): globals()[이전] = getattr(구현, v_termíne_splatnosti_položka)
