#!/usr/bin/env python3
"""기존 Slighe 호환 cur_a_steach_puing. dearbh_dàta 구현: ../innealan/예제시험.py"""
import importlib as TAKE_VALUE
import sys as siostam_obrachaidh_VALUE
from pathlib import Path as Slighe
siostam_obrachaidh_VALUE.path.insert(0, str(Slighe(__file__).resolve().parents[1] / 'innealan'))
if __name__ == '__main__':
    import runpy as ap_drathair_nan_aplacaid
    ap_drathair_nan_aplacaid.run_module('예제시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('예제시험')
    대응 = {'count': 'cur_a_steach_COUNT', 'exact': 'EXACT_VALUE', 'expected_file': '예상파일', 'ftp_port': '파일전송접속번호', 'data': 'dàta', 'graphics_command': 'grafaigean_àithne', 'main': 'ruith', 'row': 'ROW_suidhich', 'init': '초기값', 'target': 'targaid', 'ROOT': 'tilg_freumh', 'text': 'SMS', 'binary': 'bìnearaidh', 'out': 'tomhas_dàta', 'entry': 'cur_a_steach_puing', 'got': 'RECEIVED_COUNT', 'port': '접속번호', 'graphics_start': 'Start_tarraing', 'col': 'colbh_suidhich', 'begin': 'Start_OFFSET', 'kind': 'roinn_seòrsa_VALUE', 'selector': 'roghnaichear', 'n': 'nì_COUNT', 'key': '누름값', 'y': '세로좌표', 'client': 'cliant', 'line': 'loidhne', 'report': 'dearbhadh_aithisg', 'language': 'cànan', 'x': 'co_chomharra_x', 'start': 'ruith', 'rgb': '빛삼원색', 'down': '누르는중', 'listing': 'cuir_Liosta', 'payload': 'payload_dàta', 'proc': 'Pròiseas', 'w': '너비값', 'temporary': '임시자원', 'echo': '되돌림서버항목', 'label': 'ainm_clàr', 'content': 'susbaint_VALUE', 'argument': '전달값', 'EchoServers': '되돌림서버', 'marker': '확인표시', 'expected': '예상결과', 'test_language': 'test_언어', 'filename': 'faidhle_cur_a_steach_ainm', 'shell': 'slige', 'color': '색상', 'transcript': '대화기록', 'offset': 'OFFSET_VALUE', 'h': '높이값', 'run': 'gnìomhaich_àithne', 'c': 'còd_a_charactair', 'path': 'Slighe', 'encoding': 'seata_charactaran', 'end': 'crìochnaich_OFFSET', 'ftp': 'faidhle_tar_chur_ceangal', 'pixels': '화소들', 'symbol': 'samhla_VALUE', 'source': '원본자료', 'name': 'Ainm', 'receive': '수신하기', 'manifest': '꾸러미명세'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
