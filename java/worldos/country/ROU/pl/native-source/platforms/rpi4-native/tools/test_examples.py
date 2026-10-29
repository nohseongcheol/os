#!/usr/bin/env python3
"""기존 ścieżka_2 호환 punkt_wejścia. rzeczywisty_dane implementacja: ../narzędzia/예제시험.py"""
import importlib as WYCINEK_WARTOŚĆ
import sys as system_operacyjny_WARTOŚĆ
from pathlib import Path as ścieżka_2
system_operacyjny_WARTOŚĆ.path.insert(0, str(ścieżka_2(__file__).resolve().parents[1] / 'narzędzia'))
if __name__ == '__main__':
    import runpy as program_Launcher
    program_Launcher.run_module('예제시험', run_name='__main__', alter_sys=True)
else:
    implementacja = WYCINEK_WARTOŚĆ.import_module('예제시험')
    mapowanie_WARTOŚĆ = {'count': 'wpis_ILE_LICZB', 'exact': 'PORÓWNAJ_WARTOŚĆ', 'expected_file': '예상파일', 'ftp_port': 'transfer_plików_numer_portu', 'data': 'dane', 'graphics_command': 'grafika_polecenie', 'main': 'Uruchom_2', 'row': 'WIERSZ_stanowisko', 'init': '초기값', 'target': 'wartość_docelowa', 'ROOT': 'Project_korzeń', 'text': 'tekst', 'binary': 'binarny', 'out': 'KR_dane', 'entry': 'punkt_wejścia', 'got': 'KWOTA_WYKUP_ILE_LICZB', 'port': 'numer_portu', 'graphics_start': 'START_rysunek', 'col': 'kolumna_stanowisko', 'begin': 'START_przesunąć', 'kind': 'obszar_WARTOŚĆ', 'selector': 'selektor', 'n': 'towar_ILE_LICZB', 'key': '누름값', 'y': 'Y_współrzędna', 'client': 'klient', 'line': 'wiersz_wejścia', 'report': 'walidacja_Raport', 'language': 'Język', 'x': 'współrzędna_X', 'start': 'Uruchom_2', 'rgb': '빛삼원색', 'down': '누르는중', 'listing': 'wysłać_Lista', 'payload': 'ładunek_dane', 'proc': 'Proces', 'w': '너비값', 'temporary': '임시자원', 'echo': 'echo_serwer_wpis', 'label': 'nazwa_tabela', 'content': 'treść_WARTOŚĆ_cb0f2404', 'argument': '전달값', 'EchoServers': 'echo_Serwery', 'marker': 'pisak', 'expected': '예상결과', 'test_language': 'test_Język', 'filename': 'Plik_wpis_nazwa', 'shell': 'powłoka', 'color': '색상', 'transcript': 'transkrypcja', 'offset': 'przesunąć_WARTOŚĆ_450fc799', 'h': 'wymagane_wysokość_WARTOŚĆ', 'run': 'Wykonaj_polecenie', 'c': 'kod_znaku', 'path': 'ścieżka_2', 'encoding': 'zestaw_znaków', 'end': 'Koniec_przesunąć', 'ftp': 'transfer_plików_połączenie', 'pixels': '화소들', 'symbol': 'symbol_WARTOŚĆ', 'source': '원본자료', 'name': 'Nazwa', 'receive': 'odbierać_e_mail', 'manifest': 'pakiet_manifest'}
    for Wstecz_towar, bieżący_towar in mapowanie_WARTOŚĆ.items():
        if hasattr(implementacja, bieżący_towar): globals()[Wstecz_towar] = getattr(implementacja, bieżący_towar)
