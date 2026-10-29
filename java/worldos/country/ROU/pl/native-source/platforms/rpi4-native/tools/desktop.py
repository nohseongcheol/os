#!/usr/bin/env python3
"""기존 ścieżka_2 호환 punkt_wejścia. rzeczywisty_dane implementacja: ../narzędzia/Pulpit_Widok.py"""
import importlib as WYCINEK_WARTOŚĆ
import sys as system_operacyjny_WARTOŚĆ
from pathlib import Path as ścieżka_2
system_operacyjny_WARTOŚĆ.path.insert(0, str(ścieżka_2(__file__).resolve().parents[1] / 'narzędzia'))
if __name__ == '__main__':
    import runpy as program_Launcher
    program_Launcher.run_module('Pulpit_Widok', run_name='__main__', alter_sys=True)
else:
    implementacja = WYCINEK_WARTOŚĆ.import_module('Pulpit_Widok')
    mapowanie_WARTOŚĆ = {'count': 'wpis_ILE_LICZB', 'special': '특수글쇠', 'error': 'błąd', 'exact': 'PORÓWNAJ_WARTOŚĆ', 'network': 'sieć', 'closed': 'systemy_informacyjne_zamknięta', 'length': 'długość_WARTOŚĆ', 'opened': '열림', 'ftp_port': 'transfer_plików_numer_portu', 'server': 'serwer_WARTOŚĆ', 'resources': 'Zasoby', 'data': 'dane', 'shift': 'klawisz_SHIFT', 'send': 'wysłać', 'run_desktop': 'przebieg_Pulpit', 'protocol': 'sieć_ABI', 'forwards': '전달규칙들', 'host': 'host', 'text': 'tekst', 'korean': '한글여부', 'port': 'numer_portu', 'signum': 'sygnał_identyfikator', 'version': 'numer_wersji', 'parser': 'parser', 'bridge': 'mostek', 'kind': 'obszar_WARTOŚĆ', 'tail': '끝부분', 'size': 'Rozmiar', 'previous_buttons': '이전단추', 'key': '누름값', 'y': 'Y_współrzędna', 'prefix': 'interlinia_część', 'client': 'klient', 'char': 'dane_znakowe', 'work': '작업경로', 'Keyboard': 'klawiatura', 'x': 'współrzędna_X', 'down': '누르는중', 'net': 'mostek_wpis', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'argument_TABLICA', 'Hangul': '한글조합', 'chunk': 'fragment_WARTOŚĆ_652d4b53', 'proc': 'Proces', 'Desktop': 'POŁĄCZ_Pulpit', 'buttons': '단추들', 'thread': 'pracownik', 'pressed': '눌림', 'previous': 'Wstecz', 'toggle': 'zmiana_tryb', 'command': 'polecenie', 'sock': 'gniazdo_WARTOŚĆ', 'frame': 'wykonanie_kadr', 'ctrl': 'CTRL', 'path': 'ścieżka_2', 'cp': 'kodowanie_znaku', 'terminate': 'przerwać', 'security': 'Zabezpieczenia', 'vnc_port': '원격화면접속번호', 'body': 'tekst_podstawowy', 'index': 'WYSZUKAJ_INDEKS', 'exited': '종료됨', 'keysym': 'Klucz_symbol', 'output': 'produkt_wyjściowy', 'keyboard': 'klawiatura_wpis', 'interrupted': '가로채기됨', 'listener': 'odbierać_port', 'reader': 'Czytnik', 'NetworkBridge': 'mostek_3de4fe3a', 'gui': '그림화면', 'worker': 'przetwarzanie_zadanie'}
    for Wstecz_towar, bieżący_towar in mapowanie_WARTOŚĆ.items():
        if hasattr(implementacja, bieżący_towar): globals()[Wstecz_towar] = getattr(implementacja, bieżący_towar)
