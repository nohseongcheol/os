#!/usr/bin/env python3
"""기존 ścieżka_2 호환 punkt_wejścia. rzeczywisty_dane implementacja: ../narzędzia/BLD_System.py"""
import importlib as WYCINEK_WARTOŚĆ
import sys as system_operacyjny_WARTOŚĆ
from pathlib import Path as ścieżka_2
system_operacyjny_WARTOŚĆ.path.insert(0, str(ścieżka_2(__file__).resolve().parents[1] / 'narzędzia'))
if __name__ == '__main__':
    import runpy as program_Launcher
    program_Launcher.run_module('BLD_System', run_name='__main__', alter_sys=True)
else:
    implementacja = WYCINEK_WARTOŚĆ.import_module('BLD_System')
    mapowanie_WARTOŚĆ = {'network': 'sieć', 'BUILD': 'BLD_ścieżka', 'ar': 'Archiwum_narzędzie', 'build_examples': '예제만들기', 'posix': '포직스경로', 'font_data': 'czcionka_dane', 'flags': 'konfiguracja_BITS', 'a': '첫째값', 'cc': 'C_kompilator', 'args': 'argument_TABLICA', 'source_flags': '원본설정', 'ld': 'konsolidator_narzędzie', 'method': 'metoda_wpis', 'main': 'Uruchom_2', 'objcopy': 'plik_obiektu_konwerter', 'ROOT': 'Project_korzeń', 'cxx': '시플플번역기', 'includes': '포함인수', 'compiler': 'kompilator_narzędzie', 'build_users': 'Twórca_użytkownik_SPACJA', 'f': 'Plik_wpis', 'extra': '추가영역', 'exports': 'eksportować_tabela', 'jobs': '빌드작업', 'run': 'Wykonaj_polecenie', 'path': 'ścieżka_2', 'REPO': 'repozytorium_korzeń', 'tool': 'narzędzia', 'classes': 'Klasa_ścieżka', 'output': 'produkt_wyjściowy', 'samples': '예제들', 'symbol': 'symbol_WARTOŚĆ', 'source': '원본자료', 'name': 'Nazwa', 'build_network': 'Twórca_sieć', 'font_info': 'czcionka_informacje', 'manifest': 'pakiet_manifest', 'work': '작업경로'}
    for Wstecz_towar, bieżący_towar in mapowanie_WARTOŚĆ.items():
        if hasattr(implementacja, bieżący_towar): globals()[Wstecz_towar] = getattr(implementacja, bieżący_towar)
