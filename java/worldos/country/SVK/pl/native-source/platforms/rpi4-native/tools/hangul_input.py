#!/usr/bin/env python3
"""기존 ścieżka_2 호환 punkt_wejścia. rzeczywisty_dane implementacja: ../narzędzia/한글입력.py"""
import importlib as WYCINEK_WARTOŚĆ
import sys as system_operacyjny_WARTOŚĆ
from pathlib import Path as ścieżka_2
system_operacyjny_WARTOŚĆ.path.insert(0, str(ścieżka_2(__file__).resolve().parents[1] / 'narzędzia'))
if __name__ == '__main__':
    import runpy as program_Launcher
    program_Launcher.run_module('한글입력', run_name='__main__', alter_sys=True)
else:
    implementacja = WYCINEK_WARTOŚĆ.import_module('한글입력')
    mapowanie_WARTOŚĆ = {'old': 'Wstecz_towar', 'backspace': '앞글자지우기', 'committed': '확정글', 'KEYS': 'Klucz_Układ', 'self': '자신', 'FINALS': '겹끝소리', 'VOWELS': '겹가운뎃소리', 'INITIAL': '첫소리목록', 'initial': '첫소리', 'commit': 'przekazywać_kompozycja', 'feed': 'kanał_Klucz', 'vowel': '가운뎃소리', 'Hangul': '한글조합', 'SPLIT': '끝소리가르기', 'final': '끝소리', 'key': '누름값', 'send': 'wysłać', 'left': '왼쪽', 'FINAL': '끝소리목록', 'history': 'Historia', 'pair': '한쌍', 'char': 'dane_znakowe', 'VOWEL': '가운뎃소리목록', 'right': 'PRAWY', 'value': 'WARTOŚĆ', 'text': 'tekst'}
    for Wstecz_towar, bieżący_towar in mapowanie_WARTOŚĆ.items():
        if hasattr(implementacja, bieżący_towar): globals()[Wstecz_towar] = getattr(implementacja, bieżący_towar)
