#!/usr/bin/env python3
"""기존 CEĻŠ 호환 ieejas_punkts. faktisks_dati 구현: ../Rīki/예제시험.py"""
import importlib as TAKE_VALUE
import sys as operētājsistēma_VALUE
from pathlib import Path as CEĻŠ
operētājsistēma_VALUE.path.insert(0, str(CEĻŠ(__file__).resolve().parents[1] / 'Rīki'))
if __name__ == '__main__':
    import runpy as programma_palaidējs
    programma_palaidējs.run_module('예제시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('예제시험')
    kartēšana_VALUE = {'count': 'ievade_COUNT', 'exact': 'EXACT_VALUE', 'expected_file': '예상파일', 'ftp_port': 'faila_pārsūtīšana_porta_numurs', 'data': 'dati', 'graphics_command': 'grafika_komanda', 'main': 'Palaist', 'row': 'ROW_amats', 'init': '초기값', 'target': 'mērķis', 'ROOT': 'Project_sakne', 'text': 'Teksts', 'binary': 'binary', 'out': 'mērs_dati', 'entry': 'ieejas_punkts', 'got': 'RECEIVED_COUNT', 'port': 'porta_numurs', 'graphics_start': 'Sākt_zīmējums', 'col': 'COLUMN_amats', 'begin': 'Sākt_Nobīde', 'kind': 'joma_VALUE', 'selector': 'atlasītājs', 'n': 'krājums_COUNT', 'key': '누름값', 'y': '세로좌표', 'client': 'klients', 'line': 'Līniju', 'report': 'validācija_ziņot', 'language': 'Valodas', 'x': 'x_koordināta', 'start': 'Palaist', 'rgb': '빛삼원색', 'down': '누르는중', 'listing': 'sūtīt_Saraksts', 'payload': 'vērtums_dati', 'proc': 'Process', 'w': '너비값', 'temporary': '임시자원', 'echo': 'atbalss_serveris_ievade', 'label': 'nosaukums_tabula', 'content': 'Saturs_VALUE', 'argument': '전달값', 'EchoServers': 'atbalss_Serveri', 'marker': 'marķieris', 'expected': '예상결과', 'test_language': 'test_언어', 'filename': 'Fails_ievade_nosaukums', 'shell': 'čaula', 'color': '색상', 'transcript': 'transkripcija', 'offset': 'Nobīde_VALUE', 'h': '높이값', 'run': 'Izpildīt_komanda', 'c': 'koda_punkts', 'path': 'CEĻŠ', 'encoding': 'rakstzīmju_kopa', 'end': 'beigt_zvanu_Nobīde', 'ftp': 'faila_pārsūtīšana_paziņa', 'pixels': '화소들', 'symbol': 'simbols_VALUE', 'source': '원본자료', 'name': 'Nosaukums', 'receive': 'saņemt_ziņa', 'manifest': '꾸러미명세'}
    for 이전, pašreizējais_krājums in kartēšana_VALUE.items():
        if hasattr(구현, pašreizējais_krājums): globals()[이전] = getattr(구현, pašreizējais_krājums)
