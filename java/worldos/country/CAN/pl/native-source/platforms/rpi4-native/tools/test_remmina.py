#!/usr/bin/env python3
"""기존 ścieżka_2 호환 punkt_wejścia. rzeczywisty_dane implementacja: ../narzędzia/원격한글시험.py"""
import importlib as WYCINEK_WARTOŚĆ
import sys as system_operacyjny_WARTOŚĆ
from pathlib import Path as ścieżka_2
system_operacyjny_WARTOŚĆ.path.insert(0, str(ścieżka_2(__file__).resolve().parents[1] / 'narzędzia'))
if __name__ == '__main__':
    import runpy as program_Launcher
    program_Launcher.run_module('원격한글시험', run_name='__main__', alter_sys=True)
else:
    implementacja = WYCINEK_WARTOŚĆ.import_module('원격한글시험')
    mapowanie_WARTOŚĆ = {'wait': '기다리기', 'typing': '글자입력', 'start': 'Uruchom_2', 'profile': 'Profil', 'focused': 'Priorytetowe', 'serial': '직렬입출력', 'keys': '누름열', 'server': 'serwer_WARTOŚĆ', 'log': 'LOG_zapis', 'args': 'argument_TABLICA', 'deadline': 'termin_ostateczny_CZAS', 'data': 'dane', 'candidate': 'kandydat', 'logs': '기록들', 'kw': 'argument_nazwany', 'number': '수치', 'main': 'Uruchom_2', 'ready': '준비완료', 'found': 'Search_KR', 'guest': 'gość', 'ROOT': 'Project_korzeń', 'marker': 'pisak', 'text': 'tekst', 'out': 'KR_dane', 'env': 'środowisko', 'f': 'Plik_wpis', 'port': 'numer_portu', 'offset': 'przesunąć_WARTOŚĆ_450fc799', 'version': 'numer_wersji', 'p': 'dane_stanowisko', 'selector': 'selektor', 'xvfb': 'wirtualny_wyświetlać', 'display': 'wyświetlacz', 'n': 'towar_ILE_LICZB', 'key': '누름값', 'processes': '실행과정들', 'rootfs': '뿌리파일계층', 'xdo': 'wirtualny_wejście_narzędzie', 'name': 'Nazwa', 'window': 'Okno', 'report': 'walidacja_Raport', 'work': '작업경로'}
    for Wstecz_towar, bieżący_towar in mapowanie_WARTOŚĆ.items():
        if hasattr(implementacja, bieżący_towar): globals()[Wstecz_towar] = getattr(implementacja, bieżący_towar)
