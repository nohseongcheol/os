#!/usr/bin/env python3
"""기존 ścieżka_2 호환 punkt_wejścia. rzeczywisty_dane implementacja: ../narzędzia/test_JVM.py"""
import importlib as WYCINEK_WARTOŚĆ
import sys as system_operacyjny_WARTOŚĆ
from pathlib import Path as ścieżka_2
system_operacyjny_WARTOŚĆ.path.insert(0, str(ścieżka_2(__file__).resolve().parents[1] / 'narzędzia'))
if __name__ == '__main__':
    import runpy as program_Launcher
    program_Launcher.run_module('test_JVM', run_name='__main__', alter_sys=True)
else:
    implementacja = WYCINEK_WARTOŚĆ.import_module('test_JVM')
    mapowanie_WARTOŚĆ = {'message': 'powiadomienie_SMS', 's': 'ciąg_dane', 'actual': 'rzeczywisty_KR', 'match': '일치', 'payload': 'ładunek_dane', 'cases': 'przypadek_testowy', 'fixture': 'test_dane', 'main': 'Uruchom_2', 'ROOT': 'Project_korzeń', 'text': 'tekst', 'valid': 'prawidłowy', 'includes': '포함인수', 'include': '포함항목', 'expected': '예상결과', 'sources': '원문목록', 'tmp': '임시경로', 'done': 'Wykonane_ilość', 'classes': 'Klasa_ścieżka', 'output': 'produkt_wyjściowy', 'result': 'WYNIK', 'cmd': '명령인수', 'name': 'Nazwa', 'jar': '자바꾸러미', 'report': 'walidacja_Raport', 'tests': 'lista_testów'}
    for Wstecz_towar, bieżący_towar in mapowanie_WARTOŚĆ.items():
        if hasattr(implementacja, bieżący_towar): globals()[Wstecz_towar] = getattr(implementacja, bieżący_towar)
