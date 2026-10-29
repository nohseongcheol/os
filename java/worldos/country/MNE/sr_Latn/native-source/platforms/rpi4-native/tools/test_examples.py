#!/usr/bin/env python3
"""기존 putanja 호환 stavka_p. stvarni_podaci 구현: ../Alatke/예제시험.py"""
import importlib as TAKE_VALUE
import sys as operativni_sistem_VALUE
from pathlib import Path as putanja
operativni_sistem_VALUE.path.insert(0, str(putanja(__file__).resolve().parents[1] / 'Alatke'))
if __name__ == '__main__':
    import runpy as program_pokretač
    program_pokretač.run_module('예제시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('예제시험')
    mapiranje_VALUE = {'count': 'stavka_COUNT_8f7753a1', 'exact': 'EXACT_VALUE', 'expected_file': '예상파일', 'ftp_port': 'prenos_datoteka_broj_porta', 'data': 'podaci', 'graphics_command': 'grafika_komanda', 'main': 'koristiti', 'row': 'ROW_pozicija', 'init': '초기값', 'target': 'cilj', 'ROOT': 'radnja_koren', 'text': 'SMS', 'binary': 'binarni', 'out': 'KR_podaci', 'entry': 'stavka_p', 'got': 'RECEIVED_COUNT', 'port': 'broj_porta', 'graphics_start': 'START_crtež', 'col': 'COLUMN_pozicija', 'begin': 'START_Pomak', 'kind': 'oblast_VALUE', 'selector': 'birač', 'n': 'stavka_COUNT', 'key': '누름값', 'y': '세로좌표', 'client': 'klijent', 'line': 'red', 'report': 'provera_valjanosti_izveštaj', 'language': 'jezik', 'x': 'x_koordinata', 'start': 'koristiti', 'rgb': '빛삼원색', 'down': '누르는중', 'listing': 'poslati_Lista', 'payload': 'korisni_podaci_podaci', 'proc': 'Proces', 'w': '너비값', 'temporary': '임시자원', 'echo': 'eho_server_stavka', 'label': 'ime_tabela', 'content': 'Sadržaj_VALUE', 'argument': '전달값', 'EchoServers': 'eho_Serveri', 'marker': 'označivač', 'expected': '예상결과', 'test_language': 'test_언어', 'filename': 'Datoteka_stavka_ime', 'shell': 'ljuska', 'color': '색상', 'transcript': 'transkript', 'offset': 'Pomak_VALUE', 'h': '높이값', 'run': 'Izvrši_komanda', 'c': 'kôd_znaka', 'path': 'putanja', 'encoding': 'skup_znakova', 'end': 'završiti_razgovor_Pomak', 'ftp': 'prenos_datoteka_veza', 'pixels': '화소들', 'symbol': 'simbol_VALUE', 'source': '원본자료', 'name': 'ime', 'receive': 'primiti_poruka', 'manifest': '꾸러미명세'}
    for 이전, aktuelno_stavka in mapiranje_VALUE.items():
        if hasattr(구현, aktuelno_stavka): globals()[이전] = getattr(구현, aktuelno_stavka)
