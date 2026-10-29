#!/usr/bin/env python3
"""기존 ПАТЕКА 호환 внес_поен. реален_податоци 구현: ../Алатки/바탕화면시험.py"""
import importlib as TAKE_VALUE
import sys as оперативен_систем_VALUE
from pathlib import Path as ПАТЕКА
оперативен_систем_VALUE.path.insert(0, str(ПАТЕКА(__file__).resolve().parents[1] / 'Алатки'))
if __name__ == '__main__':
    import runpy as програма_стартувач
    програма_стартувач.run_module('바탕화면시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('바탕화면시험')
    대응 = {'x': 'координата_х', 'typing': '글자입력', 'message': '알림문', 'start': 'Изврши_2', 'down': '누르는중', 'exact': 'EXACT_VALUE', 'i': '순번', 'press': '글쇠누르기', 'rectangles': '사각형들', 'sym': 'симбол', 'j': '안쪽순번', 'deadline': '마감시각', 'proc': 'Процес', 'data': 'податоци', 'main': 'Изврши_2', 'w': '너비값', 'init': '초기값', 'block': 'податоци_блокирај', 'ROOT': 'Project_корен', 'text': 'Текст', 'marker': '확인표시', 'report': 'проверка_извештај', 'until': '까지', 'clipboard': 'склад_VALUE', 'dst': 'одредиште_адреса', 'seen': '본항목들', 'poll': '준비살피미', 'transcript': '대화기록', 'port': 'број_на_порта', 'offset': 'OFFSET_VALUE', 'h': '높이값', 'src': '원본주소', 'event': 'настан', 'encoding': 'збир_знаци', 'size': 'Големина', 'key': '누름값', 'pixels': '화소들', 'y': '세로좌표', 'output': '출력결과', 'symbol': 'симбол_VALUE', 'client': 'клиент', 'char': 'знак_податоци', 'rgb': '빛삼원색'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
