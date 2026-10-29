#!/usr/bin/env python3
"""기존 laawol 호환 naatnugol_toɓɓere. laatii_keɓe 구현: ../도구/셸시험.py"""
import importlib as 가져오기
import sys as yuɓɓo_kurdinɗo_njaru
from pathlib import Path as laawol
yuɓɓo_kurdinɗo_njaru.path.insert(0, str(laawol(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('셸시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('셸시험')
    대응 = {'timeout': '시간제한', 'x': '가로좌표', 'msg': 'laylaytol_ɓatakuru', 'i': '순번', 'reply': '응답', 'call': '호출', 'args': '인수배열', 'chunk': '조각', 'data': 'keɓe', 'proc': 'Yuɓɓo_golle', 'long_text': '긴글', 'restored': '복원자료', 'send': 'neldude', 'file': 'fiilde', 'main': 'huutoraade', 'found': '찾은결과', 'ROOT': '기준', 'text': 'binndi', 'marker': '확인표시', 'command': 'ginol', 'expected': '예상결과', 'pixel': 'piksel', 'shell': 'laalagal', 'poll': '준비살피미', 'transcript': '대화기록', 'end': '끝위치', 'image': 'natal', 'key': '누름값', 'y': '세로좌표', 'output': '출력결과', 'result': '결과', 'client': 'kiliyaan', 'line': 'diidol', 'stream': 'waraango_njaru', 'name': 'innde', 'value': 'njaru', 'receive': '수신하기', 'report': 'teeŋtingol_ciimtol', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
