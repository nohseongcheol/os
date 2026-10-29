#!/usr/bin/env python3
"""기존 Putanja 호환 unos_p. stvaran_podaci 구현: ../Alati/예제시험.py"""
import importlib as TAKE_VALUE
import sys as operativni_sistem_VALUE
from pathlib import Path as Putanja
operativni_sistem_VALUE.path.insert(0, str(Putanja(__file__).resolve().parents[1] / 'Alati'))
if __name__ == '__main__':
    import runpy as program_pokretač
    program_pokretač.run_module('예제시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('예제시험')
    대응 = {'count': 'unos_COUNT', 'exact': 'EXACT_VALUE', 'expected_file': '예상파일', 'ftp_port': 'fajl_prijenos_broj_priključka', 'data': 'podaci', 'graphics_command': 'grafika_komanda', 'main': 'Pokreni', 'row': 'ROW_položaj', 'init': '초기값', 'target': 'cilj', 'ROOT': 'projicirati_koijen', 'text': 'Tekst', 'binary': 'binarno', 'out': 'mjera_podaci', 'entry': 'unos_p', 'got': 'RECEIVED_COUNT', 'port': 'broj_priključka', 'graphics_start': 'START_ucrtavanje', 'col': 'COLUMN_položaj', 'begin': 'START_Pomak', 'kind': 'oblast_VALUE', 'selector': 'birač', 'n': 'stavka_COUNT', 'key': '누름값', 'y': 'Y_koordinata', 'client': 'klijent', 'line': 'Linija', 'report': 'provjera_izvještaj', 'language': 'Jezik', 'x': 'koordinata_x', 'start': 'Pokreni', 'rgb': '빛삼원색', 'down': '누르는중', 'listing': 'poslati_spisak', 'payload': 'korisni_sadržaj_podaci', 'proc': 'proces', 'w': '너비값', 'temporary': '임시자원', 'echo': '되돌림서버항목', 'label': 'naziv_tabela', 'content': 'Sadržaj_VALUE', 'argument': '전달값', 'EchoServers': '되돌림서버', 'marker': '확인표시', 'expected': '예상결과', 'test_language': 'test_언어', 'filename': 'fajl_unos_naziv', 'shell': 'ljuska', 'color': '색상', 'transcript': '대화기록', 'offset': 'Pomak_VALUE', 'h': '높이값', 'run': 'Izvrši_komanda', 'c': 'kôd_znaka', 'path': 'Putanja', 'encoding': 'skup_znakova', 'end': 'završiti_Pomak', 'ftp': 'fajl_prijenos_veza', 'pixels': '화소들', 'symbol': 'simbol_VALUE', 'source': '원본자료', 'name': 'Naziv', 'receive': '수신하기', 'manifest': '꾸러미명세'}
    for 이전, trenutno_stavka in 대응.items():
        if hasattr(구현, trenutno_stavka): globals()[이전] = getattr(구현, trenutno_stavka)
