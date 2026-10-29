#!/usr/bin/env python3
"""기존 ścieżka_2 호환 punkt_wejścia. rzeczywisty_dane implementacja: ../narzędzia/SDK_kompilować.py"""
import importlib as WYCINEK_WARTOŚĆ
import sys as system_operacyjny_WARTOŚĆ
from pathlib import Path as ścieżka_2
system_operacyjny_WARTOŚĆ.path.insert(0, str(ścieżka_2(__file__).resolve().parents[1] / 'narzędzia'))
if __name__ == '__main__':
    import runpy as program_Launcher
    program_Launcher.run_module('SDK_kompilować', run_name='__main__', alter_sys=True)
else:
    implementacja = WYCINEK_WARTOŚĆ.import_module('SDK_kompilować')
    mapowanie_WARTOŚĆ = {'compiler': 'kompilator_narzędzie', 'obj': 'plik_docelowy', 'sdk': 'zestaw_deweloperski', 'output': 'produkt_wyjściowy', 'main': 'Uruchom_2', 'elf': 'plik_wykonywalny', 'is_c': 'systemy_informacyjne_C_Język', 'parser': 'parser', 'language': 'Język', 'work': '작업경로', 'args': 'argument_TABLICA'}
    for Wstecz_towar, bieżący_towar in mapowanie_WARTOŚĆ.items():
        if hasattr(implementacja, bieżący_towar): globals()[Wstecz_towar] = getattr(implementacja, bieżący_towar)
