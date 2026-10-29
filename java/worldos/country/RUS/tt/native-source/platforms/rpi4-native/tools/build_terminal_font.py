#!/usr/bin/env python3
"""기존 Yul 호환 кертү_балл. фактик_мәгълүмат 구현: ../Кораллар/төзү_Терминал_шрифт.py"""
import importlib as TAKE_VALUE
import sys as операцион_система_VALUE
from pathlib import Path as Yul
операцион_система_VALUE.path.insert(0, str(Yul(__file__).resolve().parents[1] / 'Кораллар'))
if __name__ == '__main__':
    import runpy as кушымта_хезмәткәр
    кушымта_хезмәткәр.run_module('төзү_Терминал_шрифт', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('төзү_Терминал_шрифт')
    대응 = {'data': 'мәгълүмат', 'img': 'сызым_VALUE', 'bits': '비트들', 'x': 'X_координатасы', 'draw': '화면그리기', 'licences': '이용허락목록', 'paths': 'юл_Исемлек_4d1a5003', 'y': '세로좌표', 'main': 'эшләтү', 'src': '원본주소', 'fonts': 'шрифт_Исемлек', 'ROOT': 'экранга_җибәрү_тамыр', 'p': 'мәгълүмат_урнаштыру', 'cp': 'символ_кодлау', 'target': 'максат_кыйммәт'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
