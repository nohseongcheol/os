#!/usr/bin/env python3
"""기존 ścieżka_2 호환 punkt_wejścia. rzeczywisty_dane implementacja: ../narzędzia/자바라이브러리빌드.py"""
import importlib as WYCINEK_WARTOŚĆ
import sys as system_operacyjny_WARTOŚĆ
from pathlib import Path as ścieżka_2
system_operacyjny_WARTOŚĆ.path.insert(0, str(ścieżka_2(__file__).resolve().parents[1] / 'narzędzia'))
if __name__ == '__main__':
    import runpy as program_Launcher
    program_Launcher.run_module('자바라이브러리빌드', run_name='__main__', alter_sys=True)
else:
    implementacja = WYCINEK_WARTOŚĆ.import_module('자바라이브러리빌드')
    mapowanie_WARTOŚĆ = {'header': 'Nagłówek_WARTOŚĆ', 'sources': '원문목록', 'i': '순번', 'info': 'msinfo32_exe', 'payload': 'ładunek_dane', 'src': '원본주소', 'run': 'Wykonaj_polecenie', 'build_java_library': '자바라이브러리만들기', 'relative': 'ścieżka_względna', 'classes': 'Klasa_ścieżka', 'dist': 'dystrybucja_ścieżka', 'archive': 'Archiwum', 'output': 'produkt_wyjściowy', 'root': 'korzeń_ADRES', 'name': 'Nazwa', 'jar': '자바꾸러미', 'b': 'SEKUNDA_WARTOŚĆ', 'entries': '항목들'}
    for Wstecz_towar, bieżący_towar in mapowanie_WARTOŚĆ.items():
        if hasattr(implementacja, bieżący_towar): globals()[Wstecz_towar] = getattr(implementacja, bieżący_towar)
