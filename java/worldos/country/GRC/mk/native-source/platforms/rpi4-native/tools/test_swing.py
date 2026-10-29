#!/usr/bin/env python3
"""기존 ПАТЕКА 호환 внес_поен. реален_податоци 구현: ../Алатки/화면요소시험.py"""
import importlib as TAKE_VALUE
import sys as оперативен_систем_VALUE
from pathlib import Path as ПАТЕКА
оперативен_систем_VALUE.path.insert(0, str(ПАТЕКА(__file__).resolve().parents[1] / 'Алатки'))
if __name__ == '__main__':
    import runpy as програма_стартувач
    програма_стартувач.run_module('화면요소시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('화면요소시험')
    대응 = {'wait': '기다리기', 'x': 'координата_х', 's': 'низа_податоци', 'i': '순번', 'sel': 'избирач_a916db4e', 'seconds': '초단위', 'log': 'LOG_ред', 'data': 'податоци', 'at': '현재위치', 'send': 'испрати', 'main': 'Изврши_2', 'req': 'Барање_на_HTTP_VALUE', 'hot': 'брз_пристап_VALUE', 'pump': 'рачка_настан', 'ROOT': 'Project_корен', 'marker': '확인표시', 'b': 'SECOND_VALUE', 'command': 'Команда', 'shell': 'обвивка', 'f': 'датотека_внес', 'click': 'кликни_копче', 'k': '셋째순번', 'c': 'кодна_точка', 'r': '반환값', 'p': 'податоци_позиционирање', 'command_mode': 'наредба_MODE', 'end': 'крај_OFFSET', 'classes': 'класа_патека', 'key': '누름값', 'y': '세로좌표', 'result': 'мерка', 'report': 'проверка_извештај', 'dest': 'одредиште_VALUE_позиционирање', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
