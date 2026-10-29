#!/usr/bin/env python3
"""기존 ścieżka_2 호환 punkt_wejścia. rzeczywisty_dane implementacja: ../narzędzia/Wykonaj_Plik.py"""
import importlib as WYCINEK_WARTOŚĆ
import sys as system_operacyjny_WARTOŚĆ
from pathlib import Path as ścieżka_2
system_operacyjny_WARTOŚĆ.path.insert(0, str(ścieżka_2(__file__).resolve().parents[1] / 'narzędzia'))
if __name__ == '__main__':
    import runpy as program_Launcher
    program_Launcher.run_module('Wykonaj_Plik', run_name='__main__', alter_sys=True)
else:
    implementacja = WYCINEK_WARTOŚĆ.import_module('Wykonaj_Plik')
    mapowanie_WARTOŚĆ = {'timeout': 'wykonanie_TIMEOUT', 's': 'ciąg_dane', 'i': '순번', 'match': '일치', 'files': 'lista_plików', 'program': 'program', 'executable': 'wykonywalny_OBRAZ', 'args': 'argument_TABLICA', 'chunk': 'fragment_WARTOŚĆ_652d4b53', 'data': 'dane', 'proc': 'Proces', 'send': 'wysłać', 'main': 'Uruchom_2', 'marker': 'pisak', 'command': 'polecenie', 'include': '포함항목', 'dumped': '갈무리자료', 'run': 'Wykonaj_polecenie', 'p': 'dane_stanowisko', 'parser': 'parser', 'options': 'Opcje', 'kind': 'obszar_WARTOŚĆ', 'selector': 'selektor', 'upload_data': 'Upload_dane', 'end': 'Koniec_przesunąć', 'n': 'towar_ILE_LICZB', 'd': 'cel_dane', 'key': '누름값', 'output': 'produkt_wyjściowy', 'line': 'wiersz_wejścia', 'name': 'Nazwa', 'upload_name': 'Upload_nazwa', 'receive': 'odbierać_e_mail'}
    for Wstecz_towar, bieżący_towar in mapowanie_WARTOŚĆ.items():
        if hasattr(implementacja, bieżący_towar): globals()[Wstecz_towar] = getattr(implementacja, bieżący_towar)
