#!/usr/bin/env python3
"""기존 POZICIONI 호환 futje_p. aktual_të_dhëna 구현: ../Mjete/예제시험.py"""
import importlib as TAKE_VALUE
import sys as sistem_operativ_VALUE
from pathlib import Path as POZICIONI
sistem_operativ_VALUE.path.insert(0, str(POZICIONI(__file__).resolve().parents[1] / 'Mjete'))
if __name__ == '__main__':
    import runpy as program_hapës
    program_hapës.run_module('예제시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('예제시험')
    대응 = {'count': 'futje_COUNT', 'exact': 'EXACT_VALUE', 'expected_file': '예상파일', 'ftp_port': 'skedar_transferim_numri_i_portës', 'data': 'të_dhëna', 'graphics_command': 'figura_komandë', 'main': 'Ekzekuto', 'row': 'ROW_pozicioni', 'init': '초기값', 'target': 'objektiv', 'ROOT': 'Project_rrënjë', 'text': 'Teksti', 'binary': 'binar', 'out': 'llogaritje_të_dhëna', 'entry': 'futje_p', 'got': 'RECEIVED_COUNT', 'port': 'numri_i_portës', 'graphics_start': 'nis_vizatim', 'col': 'COLUMN_pozicioni', 'begin': 'nis_OFFSET', 'kind': 'kategori_VALUE', 'selector': 'përzgjedhësi', 'n': 'njësi_COUNT', 'key': '누름값', 'y': 'Y_koordinatë', 'client': 'klient', 'line': 'linjë', 'report': 'miratim_raport', 'language': 'Gjuha', 'x': 'koordinata_x', 'start': 'Ekzekuto', 'rgb': '빛삼원색', 'down': '누르는중', 'listing': 'dërgoj_Listë', 'payload': 'ngarkesë_e_dobishme_të_dhëna', 'proc': 'Proçes', 'w': '너비값', 'temporary': '임시자원', 'echo': '되돌림서버항목', 'label': 'emër_tabelë', 'content': 'Përmbajtje_VALUE', 'argument': '전달값', 'EchoServers': '되돌림서버', 'marker': '확인표시', 'expected': '예상결과', 'test_language': 'test_언어', 'filename': 'skedar_futje_emër', 'shell': 'pasues', 'color': '색상', 'transcript': '대화기록', 'offset': 'OFFSET_VALUE', 'h': '높이값', 'run': 'zbatoj_komandë', 'c': 'kodi_i_karakterit', 'path': 'POZICIONI', 'encoding': 'bashkësia_e_karaktereve', 'end': 'mbaroj_OFFSET', 'ftp': 'skedar_transferim_lidhje', 'pixels': '화소들', 'symbol': 'simbol_VALUE', 'source': '원본자료', 'name': 'Emër', 'receive': '수신하기', 'manifest': '꾸러미명세'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
