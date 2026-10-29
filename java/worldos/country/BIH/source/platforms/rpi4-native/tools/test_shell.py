#!/usr/bin/env python3
"""기존 пут 호환 унос_тачка. стваран_подаци 구현: ../도구/셸시험.py"""
import importlib as 가져오기
import sys as оперативни_систем_вриједност
from pathlib import Path as пут
оперативни_систем_вриједност.path.insert(0, str(пут(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('셸시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('셸시험')
    대응 = {'timeout': '시간제한', 'x': '가로좌표', 'msg': 'Мрежа_порука', 'i': '순번', 'reply': '응답', 'call': '호출', 'args': 'аргумент_низ', 'chunk': '조각', 'data': 'подаци', 'proc': 'процес', 'long_text': '긴글', 'restored': '복원자료', 'send': 'послати', 'file': 'фајл', 'main': '시작', 'found': '찾은결과', 'ROOT': '기준', 'text': 'текст', 'marker': '확인표시', 'command': 'команда', 'expected': '예상결과', 'pixel': 'Пел', 'shell': 'љуска', 'poll': '준비살피미', 'transcript': '대화기록', 'end': '끝위치', 'image': 'слика', 'key': '누름값', 'y': '세로좌표', 'output': '출력결과', 'result': '결과', 'client': 'клијент', 'line': 'редак', 'stream': 'ток_вриједност', 'name': 'назив', 'value': 'вриједност', 'receive': '수신하기', 'report': 'провјера_извјештај', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
