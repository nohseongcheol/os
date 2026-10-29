#!/usr/bin/env python3
"""기존 Yul 호환 кертү_балл. фактик_мәгълүмат 구현: ../Кораллар/үтәргә_файл.py"""
import importlib as TAKE_VALUE
import sys as операцион_система_VALUE
from pathlib import Path as Yul
операцион_система_VALUE.path.insert(0, str(Yul(__file__).resolve().parents[1] / 'Кораллар'))
if __name__ == '__main__':
    import runpy as кушымта_хезмәткәр
    кушымта_хезмәткәр.run_module('үтәргә_файл', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('үтәргә_файл')
    대응 = {'timeout': '시간제한', 's': 'юл_мәгълүмат', 'i': '순번', 'match': '일치', 'files': 'файл_Исемлек', 'program': 'кушымта', 'executable': '실행가능파일', 'args': 'аргумент_МАССИВ', 'chunk': '조각', 'data': 'мәгълүмат', 'proc': 'Процесс', 'send': 'җибәрү', 'main': 'эшләтү', 'marker': '확인표시', 'command': 'команда', 'include': '포함항목', 'dumped': '갈무리자료', 'run': 'үтәргә_команда', 'p': 'мәгълүмат_урнаштыру', 'parser': '인수해석기', 'options': 'Параметрлар', 'kind': 'категория_VALUE', 'selector': 'сайлагыч', 'upload_data': 'йөкләп_җибәрү_мәгълүмат', 'end': 'тәмамлау_OFFSET', 'n': 'элемент_COUNT', 'd': 'күчерү_урыны_мәгълүмат', 'key': '누름값', 'output': '출력결과', 'line': 'юл', 'name': 'исем', 'upload_name': 'йөкләп_җибәрү_исем', 'receive': '수신하기'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
