#!/usr/bin/env python3
"""기존 Pad 호환 inskrywing_p. werklik_data 구현: ../Nutsmiddels/예제시험.py"""
import importlib as TAKE_VALUE
import sys as bedryfstelsel_VALUE
from pathlib import Path as Pad
bedryfstelsel_VALUE.path.insert(0, str(Pad(__file__).resolve().parents[1] / 'Nutsmiddels'))
if __name__ == '__main__':
    import runpy as program_oopmaker
    program_oopmaker.run_module('예제시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('예제시험')
    대응 = {'count': 'inskrywing_COUNT', 'exact': 'EXACT_VALUE', 'expected_file': '예상파일', 'ftp_port': '파일전송접속번호', 'data': 'data', 'graphics_command': 'grafika_bevel', 'main': 'Loop', 'row': 'ry_plaas', 'init': '초기값', 'target': 'teiken', 'ROOT': 'Project_wortel', 'text': 'Teks', 'binary': 'binêr', 'out': 'maatreël_data', 'entry': 'inskrywing_p', 'got': 'RECEIVED_COUNT', 'port': '접속번호', 'graphics_start': 'BEGIN_tekening', 'col': 'kolom_plaas', 'begin': 'BEGIN_OFFSET', 'kind': 'kategorie_VALUE', 'selector': 'selekteerder', 'n': 'item_COUNT', 'key': '누름값', 'y': 'Y_koördinaat', 'client': 'kliënt', 'line': 'lyn', 'report': 'validering_verslag', 'language': 'Taal', 'x': 'x_koördinaat', 'start': 'Loop', 'rgb': '빛삼원색', 'down': '누르는중', 'listing': 'e_pos_Lys', 'payload': 'lading_data', 'proc': 'Proses', 'w': '너비값', 'temporary': '임시자원', 'echo': '되돌림서버항목', 'label': 'naam_tabel', 'content': 'Inhoud_VALUE', 'argument': '전달값', 'EchoServers': '되돌림서버', 'marker': '확인표시', 'expected': '예상결과', 'test_language': 'test_언어', 'filename': 'lêer_inskrywing_naam', 'shell': 'dop', 'color': '색상', 'transcript': '대화기록', 'offset': 'OFFSET_VALUE', 'h': '높이값', 'run': 'uitvoer_bevel', 'c': 'karakterkode', 'path': 'Pad', 'encoding': 'karakterstel', 'end': 'beëindig_OFFSET', 'ftp': 'lêer_oordra_verbinding', 'pixels': '화소들', 'symbol': 'simbool_VALUE', 'source': '원본자료', 'name': 'Naam', 'receive': '수신하기', 'manifest': '꾸러미명세'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
