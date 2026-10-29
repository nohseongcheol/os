#!/usr/bin/env python3
"""기존 laawol 호환 naatnugol_toɓɓere. laatii_keɓe 구현: ../도구/예제시험.py"""
import importlib as 가져오기
import sys as yuɓɓo_kurdinɗo_njaru
from pathlib import Path as laawol
yuɓɓo_kurdinɗo_njaru.path.insert(0, str(laawol(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('예제시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제시험')
    대응 = {'count': '항목수', 'exact': '정확한값', 'expected_file': '예상파일', 'ftp_port': '파일전송접속번호', 'data': 'keɓe', 'graphics_command': '그림명령', 'main': 'huutoraade', 'row': '행위치', 'init': '초기값', 'target': 'faandaare', 'ROOT': '기준', 'text': 'binndi', 'binary': 'biinere', 'out': '결과자료', 'entry': 'naatnugol_toɓɓere', 'got': '받은수', 'port': '접속번호', 'graphics_start': 'huɓɓude_natal', 'col': '열위치', 'begin': '시작위치', 'kind': 'kategorii_njaru', 'selector': '준비선택기', 'n': '개수', 'key': '누름값', 'y': '세로좌표', 'client': 'kiliyaan', 'line': 'diidol', 'report': 'teeŋtingol_ciimtol', 'language': '언어', 'x': '가로좌표', 'start': 'huutoraade', 'rgb': '빛삼원색', 'down': '누르는중', 'listing': 'neldude_Doggol', 'payload': '내용자료', 'proc': 'Yuɓɓo_golle', 'w': '너비값', 'temporary': '임시자원', 'echo': '되돌림서버항목', 'label': 'innde_taabal', 'content': 'loowdi_njaru', 'argument': '전달값', 'EchoServers': '되돌림서버', 'marker': '확인표시', 'expected': '예상결과', 'test_language': 'test_언어', 'filename': 'fiilde_naatnugol_innde', 'shell': 'laalagal', 'color': '색상', 'transcript': '대화기록', 'offset': '변위', 'h': '높이값', 'run': '실행', 'c': '문자값', 'path': 'laawol', 'encoding': 'mooɓre_alkule', 'end': '끝위치', 'ftp': 'fiilde_egginde_ceŋondiral', 'pixels': '화소들', 'symbol': '심볼', 'source': '원본자료', 'name': 'innde', 'receive': '수신하기', 'manifest': '꾸러미명세'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
