#!/usr/bin/env python3
"""기존 ara 호환 tāurunga_ira. tūturu_raraunga 구현: ../Ngā_Utauta/예제시험.py"""
import importlib as TAKE_uara
import sys as pūnaha_mahi_uara
from pathlib import Path as ara
pūnaha_mahi_uara.path.insert(0, str(ara(__file__).resolve().parents[1] / 'Ngā_Utauta'))
if __name__ == '__main__':
    import runpy as kaupapa_pūwhiri_taupānga
    kaupapa_pūwhiri_taupānga.run_module('예제시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_uara.import_module('예제시험')
    대응 = {'count': 'tāurunga_COUNT', 'exact': 'EXACT_uara', 'expected_file': '예상파일', 'ftp_port': '파일전송접속번호', 'data': 'raraunga', 'graphics_command': 'whakairoiro_tono', 'main': 'whakahaere', 'row': 'ROW_tūranga', 'init': '초기값', 'target': 'ūnga', 'ROOT': 'whakaatu_pūtake', 'text': 'Ngā_kupu', 'binary': 'ā_rua', 'out': 'mēhua_raraunga', 'entry': 'tāurunga_ira', 'got': 'RECEIVED_COUNT', 'port': '접속번호', 'graphics_start': 'Start_tātuhi', 'col': 'tīwae_tūranga', 'begin': 'Start_OFFSET', 'kind': 'kāwai_uara', 'selector': 'pūtīpako', 'n': 'tuemi_COUNT', 'key': '누름값', 'y': '세로좌표', 'client': 'kiritaki', 'line': 'hononga', 'report': 'whakamana_pūrongo', 'language': 'reo', 'x': 'taunga_x', 'start': 'whakahaere', 'rgb': '빛삼원색', 'down': '누르는중', 'listing': 'tuku_Rārangi', 'payload': 'tino_raraunga_raraunga', 'proc': 'Hātepe', 'w': '너비값', 'temporary': '임시자원', 'echo': '되돌림서버항목', 'label': 'ingoa_ripanga', 'content': 'Ihirangi_uara', 'argument': '전달값', 'EchoServers': '되돌림서버', 'marker': '확인표시', 'expected': '예상결과', 'test_language': 'test_언어', 'filename': 'kōnae_tāurunga_ingoa', 'shell': 'anga', 'color': '색상', 'transcript': '대화기록', 'offset': 'OFFSET_uara', 'h': '높이값', 'run': 'kawe_tono', 'c': 'waehere_pūāhua', 'path': 'ara', 'encoding': 'rōpū_pūāhua', 'end': 'mutu_OFFSET', 'ftp': 'kōnae_whakawhiti_hononga', 'pixels': '화소들', 'symbol': 'tohu_uara', 'source': '원본자료', 'name': 'Ingoa', 'receive': '수신하기', 'manifest': '꾸러미명세'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
