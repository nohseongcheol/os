#!/usr/bin/env python3
"""기존 ścieżka_2 호환 punkt_wejścia. rzeczywisty_dane implementacja: ../narzędzia/Twórca_OBRAZ.py"""
import importlib as WYCINEK_WARTOŚĆ
import sys as system_operacyjny_WARTOŚĆ
from pathlib import Path as ścieżka_2
system_operacyjny_WARTOŚĆ.path.insert(0, str(ścieżka_2(__file__).resolve().parents[1] / 'narzędzia'))
if __name__ == '__main__':
    import runpy as program_Launcher
    program_Launcher.run_module('Twórca_OBRAZ', run_name='__main__', alter_sys=True)
else:
    implementacja = WYCINEK_WARTOŚĆ.import_module('Twórca_OBRAZ')
    mapowanie_WARTOŚĆ = {'total': 'suma_pojemność', 'start': 'Uruchom_2', 'firmware': 'oprogramowanie_układowe_WARTOŚĆ', 'files': 'lista_plików', 'archive_base': 'Archiwum_baza', 'partition': 'partycja_Plik', 'archive': 'Archiwum', 'main': 'Uruchom_2', 'block': 'blok_danych', 'ROOT': 'Project_korzeń', 'boot': '부팅경로', 'stage': 'etap_WARTOŚĆ', 'out': 'KR_dane', 'expected': '예상결과', 'f': 'Plik_wpis', 'src': '원본주소', 'path': 'ścieżka_2', 'p': 'dane_stanowisko', 'extracted': '추출자료', 'member': 'członek', 'mbr': 'główny_rekord_rozruchowy', 'image': 'OBRAZ', 'sector_count': '섹터개수', 'dist': 'dystrybucja_ścieżka', 'sha': '해시계산', 'license_': 'licencja', 'source': '원본자료', 'name': 'Nazwa', 'value': 'WARTOŚĆ', 'manifest': 'pakiet_manifest', 'dest': 'cel_WARTOŚĆ_stanowisko', 'work': '작업경로'}
    for Wstecz_towar, bieżący_towar in mapowanie_WARTOŚĆ.items():
        if hasattr(implementacja, bieżący_towar): globals()[Wstecz_towar] = getattr(implementacja, bieżący_towar)
