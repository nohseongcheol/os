#!/usr/bin/env python3
"""기존 ścieżka_2 호환 punkt_wejścia. rzeczywisty_dane implementacja: ../narzędzia/Wykonaj_polecenie.py"""
import importlib as WYCINEK_WARTOŚĆ
import sys as system_operacyjny_WARTOŚĆ
from pathlib import Path as ścieżka_2
system_operacyjny_WARTOŚĆ.path.insert(0, str(ścieżka_2(__file__).resolve().parents[1] / 'narzędzia'))
if __name__ == '__main__':
    import runpy as program_Launcher
    program_Launcher.run_module('Wykonaj_polecenie', run_name='__main__', alter_sys=True)
else:
    implementacja = WYCINEK_WARTOŚĆ.import_module('Wykonaj_polecenie')
    mapowanie_WARTOŚĆ = {'supported': '지원목록', 'parser': 'parser', 'qemu': '모의기계', 'run_desktop': 'przebieg_Pulpit', 'main': 'Uruchom_2', 'host': 'host', 'status': 'Stan_WARTOŚĆ', 'NetworkBridge': 'mostek_3de4fe3a', 'ROOT': 'Project_korzeń', 'bridge': 'mostek', 'loader': 'moduł_ładujący', 'base': 'Tło_WARTOŚĆ', 'options': 'Opcje', 'binary': 'binarny', 'args': 'argument_TABLICA', 'command': 'polecenie'}
    for Wstecz_towar, bieżący_towar in mapowanie_WARTOŚĆ.items():
        if hasattr(implementacja, bieżący_towar): globals()[Wstecz_towar] = getattr(implementacja, bieżący_towar)
