#!/usr/bin/env python3
"""기존 SLÓÐ 호환 færsla_P. raun_gögn 구현: ../Verkfæri/예제시험.py"""
import importlib as TAKE_VALUE
import sys as stýrikerfi_VALUE
from pathlib import Path as SLÓÐ
stýrikerfi_VALUE.path.insert(0, str(SLÓÐ(__file__).resolve().parents[1] / 'Verkfæri'))
if __name__ == '__main__':
    import runpy as forrit_ræsir
    forrit_ræsir.run_module('예제시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('예제시험')
    vörpun_VALUE = {'count': 'færsla_COUNT', 'exact': 'EXACT_VALUE', 'expected_file': '예상파일', 'ftp_port': 'skrá_flytja_tengisnúmer', 'data': 'gögn', 'graphics_command': 'myndefni_skipun', 'main': 'Keyra_2', 'row': 'ROW_staða', 'init': '초기값', 'target': 'markmið', 'ROOT': 'verk_rót', 'text': 'Texti', 'binary': 'tvíundar', 'out': 'mæld_stærð_gögn', 'entry': 'færsla_P', 'got': 'RECEIVED_COUNT', 'port': 'tengisnúmer', 'graphics_start': 'Opna_teikning', 'col': 'COLUMN_staða', 'begin': 'Opna_OFFSET', 'kind': 'tegund_VALUE', 'selector': 'val', 'n': 'vara_COUNT', 'key': '누름값', 'y': 'Y_hnit', 'client': 'biðlari', 'line': 'Lína', 'report': 'prófun_skrá', 'language': 'Tungumál', 'x': 'x_hnit', 'start': 'Keyra_2', 'rgb': '빛삼원색', 'down': '누르는중', 'listing': 'senda_Listi', 'payload': 'farmur_gögn', 'proc': 'Ferli', 'w': '너비값', 'temporary': '임시자원', 'echo': '되돌림서버항목', 'label': 'heiti_tafla', 'content': 'Efni_VALUE', 'argument': '전달값', 'EchoServers': '되돌림서버', 'marker': '확인표시', 'expected': '예상결과', 'test_language': 'test_언어', 'filename': 'skrá_færsla_heiti', 'shell': 'skel', 'color': '색상', 'transcript': '대화기록', 'offset': 'OFFSET_VALUE', 'h': '높이값', 'run': 'keyra_skipun', 'c': 'stafkóði', 'path': 'SLÓÐ', 'encoding': 'stafamengi', 'end': 'ljúka_OFFSET', 'ftp': 'skrá_flytja_tenging', 'pixels': '화소들', 'symbol': 'tákn_VALUE', 'source': '원본자료', 'name': 'Heiti', 'receive': '수신하기', 'manifest': 'búnt_skrá'}
    for 이전, 현재 in vörpun_VALUE.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
