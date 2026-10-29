#!/usr/bin/env python3
"""기존 ПАТЕКА 호환 внес_поен. реален_податоци 구현: ../Алатки/원격한글시험.py"""
import importlib as TAKE_VALUE
import sys as оперативен_систем_VALUE
from pathlib import Path as ПАТЕКА
оперативен_систем_VALUE.path.insert(0, str(ПАТЕКА(__file__).resolve().parents[1] / 'Алатки'))
if __name__ == '__main__':
    import runpy as програма_стартувач
    програма_стартувач.run_module('원격한글시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('원격한글시험')
    대응 = {'wait': '기다리기', 'typing': '글자입력', 'start': 'Изврши_2', 'profile': 'Профил', 'focused': 'Фокусирано', 'serial': '직렬입출력', 'keys': '누름열', 'server': 'сервер_VALUE', 'log': 'LOG_ред', 'args': 'аргумент_низа', 'deadline': '마감시각', 'data': 'податоци', 'candidate': '후보', 'logs': '기록들', 'kw': '이름붙인인수', 'number': '수치', 'main': 'Изврши_2', 'ready': '준비완료', 'found': 'SEARCH_мерка', 'guest': 'гостин', 'ROOT': 'Project_корен', 'marker': '확인표시', 'text': 'Текст', 'out': 'мерка_податоци', 'env': '환경', 'f': 'датотека_внес', 'port': 'број_на_порта', 'offset': 'OFFSET_VALUE', 'version': 'број_на_верзија', 'p': 'податоци_позиционирање', 'selector': 'избирач', 'xvfb': 'виртуелен_екран', 'display': 'екран', 'n': 'ставка_COUNT', 'key': '누름값', 'processes': '실행과정들', 'rootfs': '뿌리파일계층', 'xdo': '가상입력도구', 'name': 'Име', 'window': 'прозорец', 'report': 'проверка_извештај', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
