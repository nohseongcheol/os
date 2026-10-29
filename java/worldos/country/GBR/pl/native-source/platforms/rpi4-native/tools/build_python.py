#!/usr/bin/env python3
"""기존 ścieżka_2 호환 punkt_wejścia. rzeczywisty_dane implementacja: ../narzędzia/BLD_PYTHON.py"""
import importlib as WYCINEK_WARTOŚĆ
import sys as system_operacyjny_WARTOŚĆ
from pathlib import Path as ścieżka_2
system_operacyjny_WARTOŚĆ.path.insert(0, str(ścieżka_2(__file__).resolve().parents[1] / 'narzędzia'))
if __name__ == '__main__':
    import runpy as program_Launcher
    program_Launcher.run_module('BLD_PYTHON', run_name='__main__', alter_sys=True)
else:
    implementacja = WYCINEK_WARTOŚĆ.import_module('BLD_PYTHON')
    mapowanie_WARTOŚĆ = {'ld': 'konsolidator_narzędzie', 'archive': 'Archiwum', 'SHA256': 'walidacja_skrót', 'build_python': 'Twórca_PYTHON', 'root': 'korzeń_ADRES', 'source': '원본자료', 'name': 'Nazwa', 'path': 'ścieżka_2', 'VERSION': 'wersja_WARTOŚĆ_237a4c94', 'cc': 'C_kompilator', 'tar': '타르꾸러미', 'newlib': '뉴리브포함경로', 'member': 'członek'}
    for Wstecz_towar, bieżący_towar in mapowanie_WARTOŚĆ.items():
        if hasattr(implementacja, bieżący_towar): globals()[Wstecz_towar] = getattr(implementacja, bieżący_towar)
