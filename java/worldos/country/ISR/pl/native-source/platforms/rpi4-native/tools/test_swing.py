#!/usr/bin/env python3
"""기존 ścieżka_2 호환 punkt_wejścia. rzeczywisty_dane implementacja: ../narzędzia/test_Swing.py"""
import importlib as WYCINEK_WARTOŚĆ
import sys as system_operacyjny_WARTOŚĆ
from pathlib import Path as ścieżka_2
system_operacyjny_WARTOŚĆ.path.insert(0, str(ścieżka_2(__file__).resolve().parents[1] / 'narzędzia'))
if __name__ == '__main__':
    import runpy as program_Launcher
    program_Launcher.run_module('test_Swing', run_name='__main__', alter_sys=True)
else:
    implementacja = WYCINEK_WARTOŚĆ.import_module('test_Swing')
    mapowanie_WARTOŚĆ = {'wait': '기다리기', 'x': 'współrzędna_X', 's': 'ciąg_dane', 'i': '순번', 'sel': 'selektor_a916db4e', 'seconds': '초단위', 'log': 'LOG_zapis', 'data': 'dane', 'at': 'bieżący_stanowisko', 'send': 'wysłać', 'main': 'Uruchom_2', 'req': 'żądanie_WARTOŚĆ', 'hot': 'skrót_WARTOŚĆ', 'pump': 'uchwyt_konkurs', 'ROOT': 'Project_korzeń', 'marker': 'pisak', 'b': 'SEKUNDA_WARTOŚĆ', 'command': 'polecenie', 'shell': 'powłoka', 'f': 'Plik_wpis', 'click': 'klikać_przycisk', 'k': '셋째순번', 'c': 'kod_znaku', 'r': '반환값', 'p': 'dane_stanowisko', 'command_mode': 'polecenie_tryb', 'end': 'Koniec_przesunąć', 'classes': 'Klasa_ścieżka', 'key': '누름값', 'y': 'Y_współrzędna', 'result': 'WYNIK', 'report': 'walidacja_Raport', 'dest': 'cel_WARTOŚĆ_stanowisko', 'work': '작업경로', 'qmp': '모의제어접속'}
    for Wstecz_towar, bieżący_towar in mapowanie_WARTOŚĆ.items():
        if hasattr(implementacja, bieżący_towar): globals()[Wstecz_towar] = getattr(implementacja, bieżący_towar)
