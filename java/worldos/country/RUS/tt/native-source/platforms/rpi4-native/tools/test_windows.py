#!/usr/bin/env python3
"""기존 Yul 호환 кертү_балл. фактик_мәгълүмат 구현: ../Кораллар/창시험.py"""
import importlib as TAKE_VALUE
import sys as операцион_система_VALUE
from pathlib import Path as Yul
операцион_система_VALUE.path.insert(0, str(Yul(__file__).resolve().parents[1] / 'Кораллар'))
if __name__ == '__main__':
    import runpy as кушымта_хезмәткәр
    кушымта_хезмәткәр.run_module('창시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('창시험')
    대응 = {'wait': '기다리기', 'x': 'X_координатасы', 's': 'юл_мәгълүмат', 'xy': 'координатлар_пары', 'sel': 'сайлагыч_a916db4e', 'seconds': '초단위', 'log': 'LOG_юл', 'at': '현재위치', 'send': 'җибәрү', 'main': 'эшләтү', 'req': '요청값', 'hot': 'ярлык_VALUE', 'pump': 'дескриптор_вакыйга', 'ROOT': 'экранга_җибәрү_тамыр', 'marker': '확인표시', 'b': 'SECOND_VALUE', 'command': 'команда', 'shell': 'тышча', 'f': 'файл_кертү', 'color': '색상', 'click': 'чирттерү_төймә', 'k': '셋째순번', 'c': 'символ_коды', 'r': '반환값', 'p': 'мәгълүмат_урнаштыру', 'done': '완료량', 'end': 'тәмамлау_OFFSET', 'command_mode': 'команда_MODE', 'key': '누름값', 'y': '세로좌표', 'pixels': '화소들', 'result': 'үлчәм', 'report': 'раслау_отчет', 'dest': 'күчерү_урыны_VALUE_урнаштыру', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
