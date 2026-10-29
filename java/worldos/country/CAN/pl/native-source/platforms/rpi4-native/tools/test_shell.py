#!/usr/bin/env python3
"""기존 ścieżka_2 호환 punkt_wejścia. rzeczywisty_dane implementacja: ../narzędzia/test_powłoka.py"""
import importlib as WYCINEK_WARTOŚĆ
import sys as system_operacyjny_WARTOŚĆ
from pathlib import Path as ścieżka_2
system_operacyjny_WARTOŚĆ.path.insert(0, str(ścieżka_2(__file__).resolve().parents[1] / 'narzędzia'))
if __name__ == '__main__':
    import runpy as program_Launcher
    program_Launcher.run_module('test_powłoka', run_name='__main__', alter_sys=True)
else:
    implementacja = WYCINEK_WARTOŚĆ.import_module('test_powłoka')
    mapowanie_WARTOŚĆ = {'timeout': 'wykonanie_TIMEOUT', 'x': 'współrzędna_X', 'msg': 'sieć_e_mail', 'i': '순번', 'reply': 'odpowiedź', 'call': '호출', 'args': 'argument_TABLICA', 'chunk': 'fragment_WARTOŚĆ_652d4b53', 'data': 'dane', 'proc': 'Proces', 'long_text': '긴글', 'restored': '복원자료', 'send': 'wysłać', 'file': 'nazwa_pliku', 'main': 'Uruchom_2', 'found': 'Search_KR', 'ROOT': 'Project_korzeń', 'text': 'tekst', 'marker': 'pisak', 'command': 'polecenie', 'expected': '예상결과', 'pixel': 'piksel', 'shell': 'powłoka', 'poll': '준비살피미', 'transcript': 'transkrypcja', 'end': 'Koniec_przesunąć', 'image': 'OBRAZ', 'key': '누름값', 'y': 'Y_współrzędna', 'output': 'produkt_wyjściowy', 'result': 'WYNIK', 'client': 'klient', 'line': 'wiersz_wejścia', 'stream': 'Stream_WARTOŚĆ', 'name': 'Nazwa', 'value': 'WARTOŚĆ', 'receive': 'odbierać_e_mail', 'report': 'walidacja_Raport', 'work': '작업경로', 'qmp': '모의제어접속'}
    for Wstecz_towar, bieżący_towar in mapowanie_WARTOŚĆ.items():
        if hasattr(implementacja, bieżący_towar): globals()[Wstecz_towar] = getattr(implementacja, bieżący_towar)
