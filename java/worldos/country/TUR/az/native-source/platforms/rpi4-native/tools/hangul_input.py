#!/usr/bin/env python3
"""기존 Cığır 호환 daxiletmə_p. faktiki_verilənlər 구현: ../Alətlər/한글입력.py"""
import importlib as TAKE_VALUE
import sys as əməliyyat_sistemi_VALUE
from pathlib import Path as Cığır
əməliyyat_sistemi_VALUE.path.insert(0, str(Cığır(__file__).resolve().parents[1] / 'Alətlər'))
if __name__ == '__main__':
    import runpy as proqram_işəsalma
    proqram_işəsalma.run_module('한글입력', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('한글입력')
    대응 = {'old': '이전', 'backspace': '앞글자지우기', 'committed': '확정글', 'KEYS': 'Açar_Düzüm', 'self': '자신', 'FINALS': '겹끝소리', 'VOWELS': '겹가운뎃소리', 'INITIAL': '첫소리목록', 'initial': '첫소리', 'commit': '조합확정', 'feed': 'axın_Açar', 'vowel': '가운뎃소리', 'Hangul': '한글조합', 'SPLIT': '끝소리가르기', 'final': '끝소리', 'key': '누름값', 'send': 'göndərmək', 'left': '왼쪽', 'FINAL': '끝소리목록', 'history': 'Tarixçə', 'pair': '한쌍', 'char': 'simvol_verilənlər_4d9f8719', 'VOWEL': '가운뎃소리목록', 'right': 'RIGHT', 'value': 'VALUE', 'text': 'Mətn'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
