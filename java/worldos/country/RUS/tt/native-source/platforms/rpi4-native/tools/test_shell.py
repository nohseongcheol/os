#!/usr/bin/env python3
"""기존 Yul 호환 кертү_балл. фактик_мәгълүмат 구현: ../Кораллар/셸시험.py"""
import importlib as TAKE_VALUE
import sys as операцион_система_VALUE
from pathlib import Path as Yul
операцион_система_VALUE.path.insert(0, str(Yul(__file__).resolve().parents[1] / 'Кораллар'))
if __name__ == '__main__':
    import runpy as кушымта_хезмәткәр
    кушымта_хезмәткәр.run_module('셸시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('셸시험')
    대응 = {'timeout': '시간제한', 'x': 'X_координатасы', 'msg': 'Челтәр_хәбәр', 'i': '순번', 'reply': 'җавап_бирү', 'call': '호출', 'args': 'аргумент_МАССИВ', 'chunk': '조각', 'data': 'мәгълүмат', 'proc': 'Процесс', 'long_text': '긴글', 'restored': '복원자료', 'send': 'җибәрү', 'file': 'Birem', 'main': 'эшләтү', 'found': 'Эзләү_үлчәм', 'ROOT': 'экранга_җибәрү_тамыр', 'text': 'Mäten', 'marker': '확인표시', 'command': 'команда', 'expected': '예상결과', 'pixel': 'нокта', 'shell': 'тышча', 'poll': '준비살피미', 'transcript': '대화기록', 'end': 'тәмамлау_OFFSET', 'image': 'IMAGE', 'key': '누름값', 'y': '세로좌표', 'output': '출력결과', 'result': 'үлчәм', 'client': 'клиент', 'line': 'юл', 'stream': 'агым_VALUE', 'name': 'исем', 'value': 'VALUE', 'receive': '수신하기', 'report': 'раслау_отчет', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
