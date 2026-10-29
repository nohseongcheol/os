#!/usr/bin/env python3
"""기존 ШЛЯХ 호환 увядзенне_бал. фактычны_дадзеныя 구현: ../Інструменты/셸시험.py"""
import importlib as 가져오기
import sys as аперацыйная_сістэма_значэнне
from pathlib import Path as ШЛЯХ
аперацыйная_сістэма_значэнне.path.insert(0, str(ШЛЯХ(__file__).resolve().parents[1] / 'Інструменты'))
if __name__ == '__main__':
    import runpy as праграма_выклік_праграм
    праграма_выклік_праграм.run_module('셸시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('셸시험')
    대응 = {'timeout': '시간제한', 'x': 'каардыната_x', 'msg': 'Сетка_ліст', 'i': '순번', 'reply': 'адказаць', 'call': '호출', 'args': 'аргумент_масіў', 'chunk': '조각', 'data': 'дадзеныя', 'proc': 'Працэс', 'long_text': '긴글', 'restored': '복원자료', 'send': 'адправіць', 'file': 'Файл', 'main': 'Выканаць', 'found': '찾은결과', 'ROOT': '기준', 'text': 'Тэкст', 'marker': '확인표시', 'command': 'Загад', 'expected': '예상결과', 'pixel': 'пэл', 'shell': 'абалонка', 'poll': '준비살피미', 'transcript': '대화기록', 'end': 'скончыць_Зрух', 'image': 'выява', 'key': '누름값', 'y': '세로좌표', 'output': '출력결과', 'result': '결과', 'client': 'кліент', 'line': 'лінія', 'stream': 'паток_значэнне', 'name': 'Назва', 'value': 'значэнне', 'receive': '수신하기', 'report': 'праверка_справаздача', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
