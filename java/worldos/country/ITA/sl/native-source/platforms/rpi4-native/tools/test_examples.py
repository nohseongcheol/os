#!/usr/bin/env python3
"""기존 POT 호환 vnos_p. dejanski_podatki 구현: ../Orodja/예제시험.py"""
import importlib as TAKE_VALUE
import sys as operacijski_sistem_VALUE
from pathlib import Path as POT
operacijski_sistem_VALUE.path.insert(0, str(POT(__file__).resolve().parents[1] / 'Orodja'))
if __name__ == '__main__':
    import runpy as aplikacija_zaganjalnik
    aplikacija_zaganjalnik.run_module('예제시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('예제시험')
    preslikava_VALUE = {'count': 'vnos_COUNT', 'exact': 'EXACT_VALUE', 'expected_file': '예상파일', 'ftp_port': 'prenos_datotek_številka_vrat', 'data': 'podatki', 'graphics_command': 'grafični_elementi_ukaz', 'main': 'Zaženi', 'row': 'ROW_položaj', 'init': '초기값', 'target': 'tarča', 'ROOT': 'pobuda_koren', 'text': 'Besedilo', 'binary': 'binary', 'out': 'KR_podatki', 'entry': 'vnos_p', 'got': 'RECEIVED_COUNT', 'port': 'številka_vrat', 'graphics_start': 'Start_risba', 'col': 'COLUMN_položaj', 'begin': 'Start_odmik', 'kind': 'območje_VALUE', 'selector': 'izbirnik', 'n': 'element_COUNT', 'key': '누름값', 'y': '세로좌표', 'client': 'odjemalec', 'line': 'Črtni', 'report': 'preverjanje_veljavnosti_prijavi', 'language': 'jezik', 'x': 'koordinata_x', 'start': 'Zaženi', 'rgb': '빛삼원색', 'down': '누르는중', 'listing': 'poslati_Seznam', 'payload': 'koristna_vsebina_podatki', 'proc': 'Opravilo', 'w': '너비값', 'temporary': '임시자원', 'echo': 'odmev_strežnik_vnos', 'label': 'ime_tabela', 'content': 'vsebina_VALUE', 'argument': '전달값', 'EchoServers': 'odmev_Strežniki', 'marker': 'oznaka', 'expected': '예상결과', 'test_language': 'preskusiti_jezik', 'filename': 'Datoteka_vnos_ime', 'shell': 'lupina', 'color': '색상', 'transcript': 'prepis', 'offset': 'odmik_VALUE', 'h': '높이값', 'run': 'Izvedi_ukaz', 'c': 'koda_znaka', 'path': 'POT', 'encoding': 'nabor_znakov', 'end': 'končati_klic_odmik', 'ftp': 'prenos_datotek_povezava', 'pixels': '화소들', 'symbol': 'simbol_VALUE', 'source': '원본자료', 'name': 'Ime', 'receive': 'sprejeti_sprejemati_prejeti_prejemati_e_pošta', 'manifest': '꾸러미명세'}
    for 이전, sprotno_element in preslikava_VALUE.items():
        if hasattr(구현, sprotno_element): globals()[이전] = getattr(구현, sprotno_element)
