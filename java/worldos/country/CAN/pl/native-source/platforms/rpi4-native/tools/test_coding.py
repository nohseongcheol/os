#!/usr/bin/env python3
"""기존 ścieżka_2 호환 punkt_wejścia. rzeczywisty_dane implementacja: ../narzędzia/코딩시험.py"""
import importlib as WYCINEK_WARTOŚĆ
import sys as system_operacyjny_WARTOŚĆ
from pathlib import Path as ścieżka_2
system_operacyjny_WARTOŚĆ.path.insert(0, str(ścieżka_2(__file__).resolve().parents[1] / 'narzędzia'))
if __name__ == '__main__':
    import runpy as program_Launcher
    program_Launcher.run_module('코딩시험', run_name='__main__', alter_sys=True)
else:
    implementacja = WYCINEK_WARTOŚĆ.import_module('코딩시험')
    mapowanie_WARTOŚĆ = {'out': 'KR_dane', 'expected': '예상결과', 'sdk': 'zestaw_deweloperski', 'suffix': '뒷부분', 'arc': '압축묶음', 'main': 'Uruchom_2', 'elf': 'plik_wykonywalny', 'run': 'Wykonaj_polecenie', 'name': 'Nazwa', 'path': 'ścieżka_2', 'p': 'dane_stanowisko', 'ROOT': 'Project_korzeń', 'report': 'walidacja_Raport', 'args': 'argument_TABLICA'}
    for Wstecz_towar, bieżący_towar in mapowanie_WARTOŚĆ.items():
        if hasattr(implementacja, bieżący_towar): globals()[Wstecz_towar] = getattr(implementacja, bieżący_towar)
