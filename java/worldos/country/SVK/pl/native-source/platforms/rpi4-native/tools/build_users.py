#!/usr/bin/env python3
"""기존 ścieżka_2 호환 punkt_wejścia. rzeczywisty_dane implementacja: ../narzędzia/BLD_użytkownik_SPACJA.py"""
import importlib as WYCINEK_WARTOŚĆ
import sys as system_operacyjny_WARTOŚĆ
from pathlib import Path as ścieżka_2
system_operacyjny_WARTOŚĆ.path.insert(0, str(ścieżka_2(__file__).resolve().parents[1] / 'narzędzia'))
if __name__ == '__main__':
    import runpy as program_Launcher
    program_Launcher.run_module('BLD_użytkownik_SPACJA', run_name='__main__', alter_sys=True)
else:
    implementacja = WYCINEK_WARTOŚĆ.import_module('BLD_użytkownik_SPACJA')
    mapowanie_WARTOŚĆ = {'mode': 'metoda_tryb', 'header': 'Nagłówek_WARTOŚĆ', 'i': '순번', 'build_ccompiler': 'Twórca_C_kompilator', 'ar': 'Archiwum_narzędzie', 'posix': '포직스경로', 'payload': 'ładunek_dane', 'flags': 'konfiguracja_BITS', 'cases': 'przypadek_testowy', 'cc': 'C_kompilator', 'data': 'dane', 'build_java_library': '자바라이브러리만들기', 'ld': 'konsolidator_narzędzie', 'repo': 'repozytorium_ścieżka', 'build_python': 'Twórca_PYTHON', 'inc': '포함경로', 'argument': '전달값', 'text': 'tekst', 'headers': 'Nagłówek_Lista', 'cxx': '시플플번역기', 'valid': 'prawidłowy', 'build': 'BLD', 'build_users': 'Twórca_użytkownik_SPACJA', 'compiler': 'kompilator_narzędzie', 'uzlib': '압축해제경로', 'extra': '추가영역', 'phoff': 'program_Nagłówek_przesunąć', 'offset': 'przesunąć_WARTOŚĆ_450fc799', 'text_address': 'polecenie_ADRES', 'abi': 'Połącz_ABI', 'assembly': 'zestaw', 'run': 'Wykonaj_polecenie', 'path': 'ścieżka_2', 'p': 'dane_stanowisko', 'changed': '바뀐자료', 'n': 'towar_ILE_LICZB', 'flag': 'Ustawienia_WARTOŚĆ', 'index': 'WYSZUKAJ_INDEKS', 'classes': 'Klasa_ścieżka', 'output': 'produkt_wyjściowy', 'loads': '적재구획', 'data_address': 'dane_ADRES', 'symbol': 'symbol_WARTOŚĆ', 'root': 'korzeń_ADRES', 'patches': '수정사항', 'source': '원본자료', 'sizes': '크기목록', 'blobs': '탑재덩이들', 'name': 'Nazwa', 'value': 'WARTOŚĆ', 'fmt': 'format_932e03c8', 'work': '작업경로'}
    for Wstecz_towar, bieżący_towar in mapowanie_WARTOŚĆ.items():
        if hasattr(implementacja, bieżący_towar): globals()[Wstecz_towar] = getattr(implementacja, bieżący_towar)
