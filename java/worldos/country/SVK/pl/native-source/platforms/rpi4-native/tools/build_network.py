#!/usr/bin/env python3
"""기존 ścieżka_2 호환 punkt_wejścia. rzeczywisty_dane implementacja: ../narzędzia/BLD_sieć.py"""
import importlib as WYCINEK_WARTOŚĆ
import sys as system_operacyjny_WARTOŚĆ
from pathlib import Path as ścieżka_2
system_operacyjny_WARTOŚĆ.path.insert(0, str(ścieżka_2(__file__).resolve().parents[1] / 'narzędzia'))
if __name__ == '__main__':
    import runpy as program_Launcher
    program_Launcher.run_module('BLD_sieć', run_name='__main__', alter_sys=True)
else:
    implementacja = WYCINEK_WARTOŚĆ.import_module('BLD_sieć')
    mapowanie_WARTOŚĆ = {'obj': 'plik_docelowy', 'objects': 'cel_Files', 'library': 'biblioteka', 'output': 'produkt_wyjściowy', 'port': 'numer_portu', 'root': 'korzeń_ADRES', 'files': 'lista_plików', 'source': '원본자료', 'run': 'Wykonaj_polecenie', 'flags': 'konfiguracja_BITS', 'path': 'ścieżka_2', 'build_network': 'Twórca_sieć', 'cc': 'C_kompilator', 'ar': 'Archiwum_narzędzie'}
    for Wstecz_towar, bieżący_towar in mapowanie_WARTOŚĆ.items():
        if hasattr(implementacja, bieżący_towar): globals()[Wstecz_towar] = getattr(implementacja, bieżący_towar)
