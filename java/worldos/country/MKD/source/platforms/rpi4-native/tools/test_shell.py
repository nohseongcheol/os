#!/usr/bin/env python3
"""기존 ПАТЕКА 호환 внес_поен. реален_податоци 구현: ../Алатки/셸시험.py"""
import importlib as TAKE_VALUE
import sys as оперативен_систем_VALUE
from pathlib import Path as ПАТЕКА
оперативен_систем_VALUE.path.insert(0, str(ПАТЕКА(__file__).resolve().parents[1] / 'Алатки'))
if __name__ == '__main__':
    import runpy as програма_стартувач
    програма_стартувач.run_module('셸시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('셸시험')
    대응 = {'timeout': '시간제한', 'x': 'координата_х', 'msg': 'Мрежа_порака', 'i': '순번', 'reply': 'одговори', 'call': '호출', 'args': 'аргумент_низа', 'chunk': '조각', 'data': 'податоци', 'proc': 'Процес', 'long_text': '긴글', 'restored': '복원자료', 'send': 'испрати', 'file': 'Датотека', 'main': 'Изврши_2', 'found': 'SEARCH_мерка', 'ROOT': 'Project_корен', 'text': 'Текст', 'marker': '확인표시', 'command': 'Команда', 'expected': '예상결과', 'pixel': 'пиксел', 'shell': 'обвивка', 'poll': '준비살피미', 'transcript': '대화기록', 'end': 'крај_OFFSET', 'image': 'IMAGE', 'key': '누름값', 'y': '세로좌표', 'output': '출력결과', 'result': 'мерка', 'client': 'клиент', 'line': 'ред', 'stream': 'Stream_VALUE', 'name': 'Име', 'value': 'VALUE', 'receive': '수신하기', 'report': 'проверка_извештај', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
