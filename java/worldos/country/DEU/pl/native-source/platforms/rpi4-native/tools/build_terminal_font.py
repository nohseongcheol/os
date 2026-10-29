#!/usr/bin/env python3
"""기존 ścieżka_2 호환 punkt_wejścia. rzeczywisty_dane implementacja: ../narzędzia/BLD_Terminal_czcionka.py"""
import importlib as WYCINEK_WARTOŚĆ
import sys as system_operacyjny_WARTOŚĆ
from pathlib import Path as ścieżka_2
system_operacyjny_WARTOŚĆ.path.insert(0, str(ścieżka_2(__file__).resolve().parents[1] / 'narzędzia'))
if __name__ == '__main__':
    import runpy as program_Launcher
    program_Launcher.run_module('BLD_Terminal_czcionka', run_name='__main__', alter_sys=True)
else:
    implementacja = WYCINEK_WARTOŚĆ.import_module('BLD_Terminal_czcionka')
    mapowanie_WARTOŚĆ = {'data': 'dane', 'img': 'rysunek_WARTOŚĆ', 'bits': 'BITS_Lista', 'x': 'współrzędna_X', 'draw': '화면그리기', 'licences': '이용허락목록', 'paths': 'ścieżka_Lista', 'y': 'Y_współrzędna', 'main': 'Uruchom_2', 'src': '원본주소', 'fonts': 'czcionka_Lista', 'ROOT': 'Project_korzeń', 'p': 'dane_stanowisko', 'cp': 'kodowanie_znaku', 'target': 'wartość_docelowa'}
    for Wstecz_towar, bieżący_towar in mapowanie_WARTOŚĆ.items():
        if hasattr(implementacja, bieżący_towar): globals()[Wstecz_towar] = getattr(implementacja, bieżący_towar)
