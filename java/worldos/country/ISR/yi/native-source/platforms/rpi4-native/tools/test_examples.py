#!/usr/bin/env python3
"""기존 경로 호환 진입점. 실제 구현: ../도구/예제시험.py"""
import importlib as 가져오기
import sys as 체계
from pathlib import Path as 경로
체계.path.insert(0, str(경로(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('예제시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제시험')
    대응 = {'count': '항목수', 'exact': '정확한값', 'expected_file': '예상파일', 'ftp_port': '파일전송접속번호', 'data': '자료', 'graphics_command': '그림명령', 'main': '시작', 'row': '행위치', 'init': '초기값', 'target': '대상', 'ROOT': '기준', 'text': 'טעקסט', 'binary': '실행바이너리', 'out': '결과자료', 'entry': '진입점', 'got': '받은수', 'port': '접속번호', 'graphics_start': '그림시작', 'col': '열위치', 'begin': '시작위치', 'kind': '분류', 'selector': '준비선택기', 'n': '개수', 'key': '누름값', 'y': '세로좌표', 'client': '접속자', 'line': '줄', 'report': '검증기록', 'language': '언어', 'x': '가로좌표', 'start': '시작', 'rgb': '빛삼원색', 'down': '누르는중', 'listing': '목록보내기', 'payload': '내용자료', 'proc': '실행과정', 'w': '너비값', 'temporary': '임시자원', 'echo': '되돌림서버항목', 'label': '이름표', 'content': '내용', 'argument': '전달값', 'EchoServers': '되돌림서버', 'marker': '확인표시', 'expected': '예상결과', 'test_language': 'test_언어', 'filename': '파일이름', 'shell': '셸', 'color': '색상', 'transcript': '대화기록', 'offset': '변위', 'h': '높이값', 'run': '실행', 'c': '문자값', 'path': '경로', 'encoding': '문자부호', 'end': '끝위치', 'ftp': '파일전송접속', 'pixels': '화소들', 'symbol': '심볼', 'source': '원본자료', 'name': 'נאָמען', 'receive': '수신하기', 'manifest': '꾸러미명세'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
