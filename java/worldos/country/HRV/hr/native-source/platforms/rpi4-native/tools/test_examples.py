#!/usr/bin/env python3
"""기존 PUTANJA 호환 unos_p. stvaran_podaci 구현: ../Alati/예제시험.py"""
import importlib as TAKE_VALUE
import sys as operacijski_sustav_VALUE
from pathlib import Path as PUTANJA
operacijski_sustav_VALUE.path.insert(0, str(PUTANJA(__file__).resolve().parents[1] / 'Alati'))
if __name__ == '__main__':
    import runpy as program_pokretač
    program_pokretač.run_module('예제시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('예제시험')
    mapiranje_VALUE = {'count': 'unos_COUNT', 'exact': 'EXACT_VALUE', 'expected_file': '예상파일', 'ftp_port': 'prijenos_datoteka_broj_priključka', 'data': 'podaci', 'graphics_command': 'grafika_naredba', 'main': 'Pokreni', 'row': 'ROW_položaj', 'init': '초기값', 'target': 'cilj', 'ROOT': 'akcija_korijen', 'text': 'Tekst', 'binary': 'binarni_podaci', 'out': 'KR_podaci', 'entry': 'unos_p', 'got': 'RECEIVED_COUNT', 'port': 'broj_priključka', 'graphics_start': 'START_crtež', 'col': 'COLUMN_položaj', 'begin': 'START_pomak', 'kind': 'područje_VALUE', 'selector': 'odabirač', 'n': 'artikl_COUNT', 'key': '누름값', 'y': '세로좌표', 'client': 'klijent', 'line': 'red', 'report': 'provjera_izvješće', 'language': 'Jezik', 'x': 'koordinata_x', 'start': 'Pokreni', 'rgb': '빛삼원색', 'down': '누르는중', 'listing': 'slati_Popis', 'payload': 'korisni_podaci_podaci', 'proc': 'Proces', 'w': '너비값', 'temporary': '임시자원', 'echo': 'eho_server_unos', 'label': 'naziv_tablica', 'content': 'Sadržaj_VALUE', 'argument': '전달값', 'EchoServers': 'eho_Poslužitelji', 'marker': 'marker', 'expected': '예상결과', 'test_language': 'test_언어', 'filename': 'Datoteka_unos_naziv', 'shell': 'ljuska', 'color': '색상', 'transcript': 'transkript', 'offset': 'pomak_VALUE', 'h': '높이값', 'run': 'Izvrši_naredba', 'c': 'kodna_točka', 'path': 'PUTANJA', 'encoding': 'skup_znakova', 'end': 'završiti_razgovor_pomak', 'ftp': 'prijenos_datoteka_veza', 'pixels': '화소들', 'symbol': 'simbol_VALUE', 'source': '원본자료', 'name': 'Ime', 'receive': 'primiti_poruka', 'manifest': '꾸러미명세'}
    for 이전, redovno_artikl in mapiranje_VALUE.items():
        if hasattr(구현, redovno_artikl): globals()[이전] = getattr(구현, redovno_artikl)
