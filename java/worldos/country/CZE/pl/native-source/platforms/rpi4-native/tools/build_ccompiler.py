#!/usr/bin/env python3
"""기존 ścieżka_2 호환 punkt_wejścia. rzeczywisty_dane implementacja: ../narzędzia/BLD_C_kompilator.py"""
import importlib as WYCINEK_WARTOŚĆ
import sys as system_operacyjny_WARTOŚĆ
from pathlib import Path as ścieżka_2
system_operacyjny_WARTOŚĆ.path.insert(0, str(ścieżka_2(__file__).resolve().parents[1] / 'narzędzia'))
if __name__ == '__main__':
    import runpy as program_Launcher
    program_Launcher.run_module('BLD_C_kompilator', run_name='__main__', alter_sys=True)
else:
    implementacja = WYCINEK_WARTOŚĆ.import_module('BLD_C_kompilator')
    mapowanie_WARTOŚĆ = {'out': 'KR_dane', 'builtins': '내장연산', 'header': 'Nagłówek_WARTOŚĆ', 'sdk': 'zestaw_deweloperski', 'build_ccompiler': 'Twórca_C_kompilator', 'i': '순번', 'elf': 'plik_wykonywalny', 'run': 'Wykonaj_polecenie', 'flags': 'konfiguracja_BITS', 'path': 'ścieżka_2', 'p': 'dane_stanowisko', 'cc': 'C_kompilator', 'obj': 'plik_docelowy', 'flag': 'Ustawienia_WARTOŚĆ', 'ld': 'konsolidator_narzędzie', 'objects': 'cel_Files', 'repo': 'repozytorium_ścieżka', 'v': '임시값', 'upstream': 'nadrzędny_99f91985', 'root': 'korzeń_ADRES', 'assets': '탑재자료', 'source': '원본자료', 'name': 'Nazwa', 'includes': '포함인수'}
    for Wstecz_towar, bieżący_towar in mapowanie_WARTOŚĆ.items():
        if hasattr(implementacja, bieżący_towar): globals()[Wstecz_towar] = getattr(implementacja, bieżący_towar)
