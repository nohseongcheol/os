#!/usr/bin/env python3
"""기존 LLWYBR 호환 cofnod_p. go_iawn_data 구현: ../Offer/예제시험.py"""
import importlib as TAKE_VALUE
import sys as system_weithredu_VALUE
from pathlib import Path as LLWYBR
system_weithredu_VALUE.path.insert(0, str(LLWYBR(__file__).resolve().parents[1] / 'Offer'))
if __name__ == '__main__':
    import runpy as Rhaglen_lansiwr
    Rhaglen_lansiwr.run_module('예제시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('예제시험')
    대응 = {'count': 'cofnod_COUNT', 'exact': 'EXACT_VALUE', 'expected_file': '예상파일', 'ftp_port': 'ffeil_trosglwyddo_rhif_porth', 'data': 'data', 'graphics_command': 'graffeg_gorchymyn', 'main': 'Gweithredu_2', 'row': 'ROW_safle', 'init': '초기값', 'target': 'targed', 'ROOT': 'prosiect_gwraidd', 'text': 'Testun', 'binary': 'deuaidd', 'out': 'mesur_data', 'entry': 'cofnod_p', 'got': 'RECEIVED_COUNT', 'port': 'rhif_porth', 'graphics_start': 'START_lluniad', 'col': 'COLUMN_safle', 'begin': 'START_OFFSET', 'kind': 'ardal_VALUE', 'selector': 'dewisydd', 'n': 'eitem_COUNT', 'key': '누름값', 'y': 'Y_cyfesuryn', 'client': 'cleient', 'line': 'llinell', 'report': 'dilysu_adrodd', 'language': 'Iaith', 'x': 'cyfesuryn_x', 'start': 'Gweithredu_2', 'rgb': '빛삼원색', 'down': '누르는중', 'listing': 'anfon_Rhestr', 'payload': 'llwyth_uchaf_data', 'proc': 'Proses', 'w': '너비값', 'temporary': '임시자원', 'echo': '되돌림서버항목', 'label': 'enw_tabl', 'content': 'Cynnwys_VALUE', 'argument': '전달값', 'EchoServers': '되돌림서버', 'marker': '확인표시', 'expected': '예상결과', 'test_language': 'test_언어', 'filename': 'ffeil_cofnod_enw', 'shell': 'cragen', 'color': '색상', 'transcript': '대화기록', 'offset': 'OFFSET_VALUE', 'h': '높이값', 'run': 'Gweithredu_gorchymyn', 'c': 'cod_nod', 'path': 'LLWYBR', 'encoding': 'set_nodau', 'end': 'gorffen_OFFSET', 'ftp': 'ffeil_trosglwyddo_cyswllt', 'pixels': '화소들', 'symbol': 'symbol_VALUE', 'source': '원본자료', 'name': 'Enw', 'receive': '수신하기', 'manifest': '꾸러미명세'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
