#!/usr/bin/env python3
"""기존 ścieżka_2 호환 punkt_wejścia. rzeczywisty_dane implementacja: ../narzędzia/eksportować_SDK.py"""
import importlib as WYCINEK_WARTOŚĆ
import sys as system_operacyjny_WARTOŚĆ
from pathlib import Path as ścieżka_2
system_operacyjny_WARTOŚĆ.path.insert(0, str(ścieżka_2(__file__).resolve().parents[1] / 'narzędzia'))
if __name__ == '__main__':
    import runpy as program_Launcher
    program_Launcher.run_module('eksportować_SDK', run_name='__main__', alter_sys=True)
else:
    implementacja = WYCINEK_WARTOŚĆ.import_module('eksportować_SDK')
    mapowanie_WARTOŚĆ = {'out': 'KR_dane', 'obj': 'plik_docelowy', 'relative': 'ścieżka_względna', 'compiler_archive': 'kompilator_Archiwum', 'sdk': 'zestaw_deweloperski', 'dist': 'dystrybucja_ścieżka', 'archive': 'Archiwum', 'main': 'Uruchom_2', 'posix': '포직스경로', 'files': 'lista_plików', 'source': '원본자료', 'name': 'Nazwa', 'target': 'wartość_docelowa', 'ROOT': 'Project_korzeń', 'destination': 'cel_dane_ADRES', 'manifest': 'pakiet_manifest', 'work': '작업경로'}
    for Wstecz_towar, bieżący_towar in mapowanie_WARTOŚĆ.items():
        if hasattr(implementacja, bieżący_towar): globals()[Wstecz_towar] = getattr(implementacja, bieżący_towar)
