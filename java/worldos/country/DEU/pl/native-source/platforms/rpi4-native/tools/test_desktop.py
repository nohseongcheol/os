#!/usr/bin/env python3
"""기존 ścieżka_2 호환 punkt_wejścia. rzeczywisty_dane implementacja: ../narzędzia/test_Pulpit.py"""
import importlib as WYCINEK_WARTOŚĆ
import sys as system_operacyjny_WARTOŚĆ
from pathlib import Path as ścieżka_2
system_operacyjny_WARTOŚĆ.path.insert(0, str(ścieżka_2(__file__).resolve().parents[1] / 'narzędzia'))
if __name__ == '__main__':
    import runpy as program_Launcher
    program_Launcher.run_module('test_Pulpit', run_name='__main__', alter_sys=True)
else:
    implementacja = WYCINEK_WARTOŚĆ.import_module('test_Pulpit')
    mapowanie_WARTOŚĆ = {'x': 'współrzędna_X', 'typing': '글자입력', 'message': 'powiadomienie_SMS', 'start': 'Uruchom_2', 'down': '누르는중', 'exact': 'PORÓWNAJ_WARTOŚĆ', 'i': '순번', 'press': '글쇠누르기', 'rectangles': '사각형들', 'sym': 'symbol', 'j': '안쪽순번', 'deadline': 'termin_ostateczny_CZAS', 'proc': 'Proces', 'data': 'dane', 'main': 'Uruchom_2', 'w': '너비값', 'init': '초기값', 'block': 'blok_danych', 'ROOT': 'Project_korzeń', 'text': 'tekst', 'marker': 'pisak', 'report': 'walidacja_Raport', 'until': '까지', 'clipboard': 'schowek_WARTOŚĆ', 'dst': 'cel_ADRES_08bbd577', 'seen': '본항목들', 'poll': '준비살피미', 'transcript': 'transkrypcja', 'port': 'numer_portu', 'offset': 'przesunąć_WARTOŚĆ_450fc799', 'h': 'wymagane_wysokość_WARTOŚĆ', 'src': '원본주소', 'event': 'Wydarzenie', 'encoding': 'zestaw_znaków', 'size': 'Rozmiar', 'key': '누름값', 'pixels': '화소들', 'y': 'Y_współrzędna', 'output': 'produkt_wyjściowy', 'symbol': 'symbol_WARTOŚĆ', 'client': 'klient', 'char': 'dane_znakowe', 'rgb': '빛삼원색'}
    for Wstecz_towar, bieżący_towar in mapowanie_WARTOŚĆ.items():
        if hasattr(implementacja, bieżący_towar): globals()[Wstecz_towar] = getattr(implementacja, bieżący_towar)
