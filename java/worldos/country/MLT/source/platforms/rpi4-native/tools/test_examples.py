#!/usr/bin/env python3
"""기존 mogħdija 호환 entrata_punt. attwali_data 구현: ../Għodod/예제시험.py"""
import importlib as TAKE_VALUE
import sys as sistema_operattiva_VALUE
from pathlib import Path as mogħdija
sistema_operattiva_VALUE.path.insert(0, str(mogħdija(__file__).resolve().parents[1] / 'Għodod'))
if __name__ == '__main__':
    import runpy as programm_ġabra_ta_apps
    programm_ġabra_ta_apps.run_module('예제시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('예제시험')
    대응 = {'count': 'entrata_COUNT', 'exact': 'EXACT_VALUE', 'expected_file': '예상파일', 'ftp_port': '파일전송접속번호', 'data': 'data', 'graphics_command': 'grafika_kmand', 'main': 'serje', 'row': 'ROW_pożizzjoni', 'init': '초기값', 'target': 'mira', 'ROOT': 'pprojetta_għerq', 'text': 'SMS', 'binary': 'binarju', 'out': 'miżura_data', 'entry': 'entrata_punt', 'got': 'RECEIVED_COUNT', 'port': '접속번호', 'graphics_start': 'Bidu_tpinġija', 'col': 'COLUMN_pożizzjoni', 'begin': 'Bidu_OFFSET', 'kind': 'kategorija_VALUE', 'selector': 'selettur', 'n': 'element_COUNT', 'key': '누름값', 'y': '세로좌표', 'client': 'klijent', 'line': 'linja', 'report': 'validazzjoni_rapport', 'language': 'Lingwa', 'x': 'koordinat_x', 'start': 'serje', 'rgb': '빛삼원색', 'down': '누르는중', 'listing': 'bagħat_Lista', 'payload': 'payload_data', 'proc': 'Proċess', 'w': '너비값', 'temporary': '임시자원', 'echo': '되돌림서버항목', 'label': 'isem_tabella', 'content': 'Kontenut_VALUE', 'argument': '전달값', 'EchoServers': '되돌림서버', 'marker': '확인표시', 'expected': '예상결과', 'test_language': 'test_언어', 'filename': 'fajl_entrata_isem', 'shell': 'shell', 'color': '색상', 'transcript': '대화기록', 'offset': 'OFFSET_VALUE', 'h': '높이값', 'run': 'eżegwixxa_kmand', 'c': 'kodiċi_tal_karattru', 'path': 'mogħdija', 'encoding': 'sett_ta_karattri', 'end': 'ttermina_OFFSET', 'ftp': 'fajl_trasferiment_konnessjoni', 'pixels': '화소들', 'symbol': 'simbolu_VALUE', 'source': '원본자료', 'name': 'isem', 'receive': '수신하기', 'manifest': '꾸러미명세'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
