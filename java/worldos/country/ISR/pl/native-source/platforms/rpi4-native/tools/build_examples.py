#!/usr/bin/env python3
"""기존 ścieżka_2 호환 punkt_wejścia. rzeczywisty_dane implementacja: ../narzędzia/예제빌드.py"""
import importlib as WYCINEK_WARTOŚĆ
import sys as system_operacyjny_WARTOŚĆ
from pathlib import Path as ścieżka_2
system_operacyjny_WARTOŚĆ.path.insert(0, str(ścieżka_2(__file__).resolve().parents[1] / 'narzędzia'))
if __name__ == '__main__':
    import runpy as program_Launcher
    program_Launcher.run_module('예제빌드', run_name='__main__', alter_sys=True)
else:
    implementacja = WYCINEK_WARTOŚĆ.import_module('예제빌드')
    mapowanie_WARTOŚĆ = {'out': 'KR_dane', 'build_examples': '예제만들기', 'files': 'lista_plików', 'java': '자바실행', 'run': 'Wykonaj_polecenie', 'path': 'ścieżka_2', 'p': 'dane_stanowisko', 'readme': 'plik_README', 'build_java_library': '자바라이브러리만들기', 'code': 'instrukcja_SEKWENCJA', 'index': 'WYSZUKAJ_INDEKS', 'classes': 'Klasa_ścieżka', 'repo': 'repozytorium_ścieżka', 'root': 'korzeń_ADRES', 'content': 'treść_WARTOŚĆ_cb0f2404', 'source': '원본자료', 'name': 'Nazwa', 'target': 'wartość_docelowa', 'manifest': 'pakiet_manifest', 'language': 'Język'}
    for Wstecz_towar, bieżący_towar in mapowanie_WARTOŚĆ.items():
        if hasattr(implementacja, bieżący_towar): globals()[Wstecz_towar] = getattr(implementacja, bieżący_towar)
