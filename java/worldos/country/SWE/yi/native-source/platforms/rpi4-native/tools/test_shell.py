#!/usr/bin/env python3
"""기존 경로 호환 진입점. 실제 구현: ../도구/셸시험.py"""
import importlib as 가져오기
import sys as 체계
from pathlib import Path as 경로
체계.path.insert(0, str(경로(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('셸시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('셸시험')
    대응 = {'timeout': '시간제한', 'x': '가로좌표', 'msg': '통신문', 'i': '순번', 'reply': '응답', 'call': '호출', 'args': '인수배열', 'chunk': '조각', 'data': '자료', 'proc': '실행과정', 'long_text': '긴글', 'restored': '복원자료', 'send': '보내기', 'file': 'טעקע', 'main': '시작', 'found': '찾은결과', 'ROOT': '기준', 'text': 'טעקסט', 'marker': '확인표시', 'command': '명령', 'expected': '예상결과', 'pixel': '화소', 'shell': '셸', 'poll': '준비살피미', 'transcript': '대화기록', 'end': '끝위치', 'image': '실행영상', 'key': '누름값', 'y': '세로좌표', 'output': '출력결과', 'result': '결과', 'client': '접속자', 'line': '줄', 'stream': '흐름', 'name': 'נאָמען', 'value': '값', 'receive': '수신하기', 'report': '검증기록', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
