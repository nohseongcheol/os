#!/usr/bin/env python3
"""기존 ШЛЯХ 호환 увядзенне_бал. фактычны_дадзеныя 구현: ../Інструменты/바탕화면시험.py"""
import importlib as 가져오기
import sys as аперацыйная_сістэма_значэнне
from pathlib import Path as ШЛЯХ
аперацыйная_сістэма_значэнне.path.insert(0, str(ШЛЯХ(__file__).resolve().parents[1] / 'Інструменты'))
if __name__ == '__main__':
    import runpy as праграма_выклік_праграм
    праграма_выклік_праграм.run_module('바탕화면시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('바탕화면시험')
    대응 = {'x': 'каардыната_x', 'typing': '글자입력', 'message': '알림문', 'start': 'Выканаць', 'down': '누르는중', 'exact': '정확한값', 'i': '순번', 'press': '글쇠누르기', 'rectangles': '사각형들', 'sym': 'сімвал', 'j': '안쪽순번', 'deadline': '마감시각', 'proc': 'Працэс', 'data': 'дадзеныя', 'main': 'Выканаць', 'w': '너비값', 'init': '초기값', 'block': 'дадзеныя_блакіраваць', 'ROOT': '기준', 'text': 'Тэкст', 'marker': '확인표시', 'report': 'праверка_справаздача', 'until': '까지', 'clipboard': 'буфер_абмену_значэнне', 'dst': 'прызначэнне_адрас', 'seen': '본항목들', 'poll': '준비살피미', 'transcript': '대화기록', 'port': 'нумар_порта', 'offset': 'Зрух_значэнне', 'h': '높이값', 'src': '원본주소', 'event': 'Падзея', 'encoding': 'набор_сімвалаў', 'size': 'Памер', 'key': '누름값', 'pixels': '화소들', 'y': '세로좌표', 'output': '출력결과', 'symbol': 'сімвал_значэнне', 'client': 'кліент', 'char': 'сімвал_дадзеныя_4d9f8719', 'rgb': '빛삼원색'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
