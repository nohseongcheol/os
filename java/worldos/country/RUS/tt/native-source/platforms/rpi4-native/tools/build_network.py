#!/usr/bin/env python3
"""기존 Yul 호환 кертү_балл. фактик_мәгълүмат 구현: ../Кораллар/төзү_Челтәр.py"""
import importlib as TAKE_VALUE
import sys as операцион_система_VALUE
from pathlib import Path as Yul
операцион_система_VALUE.path.insert(0, str(Yul(__file__).resolve().parents[1] / 'Кораллар'))
if __name__ == '__main__':
    import runpy as кушымта_хезмәткәр
    кушымта_хезмәткәр.run_module('төзү_Челтәр', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('төзү_Челтәр')
    대응 = {'obj': 'максат_файл', 'objects': 'күчерү_урыны_Файллар', 'library': 'библиотека', 'output': '출력결과', 'port': '접속번호', 'root': 'тамыр_адрес', 'files': 'файл_Исемлек', 'source': '원본자료', 'run': 'үтәргә_команда', 'flags': '설정비트', 'path': 'Yul', 'build_network': 'Төзү_Челтәр', 'cc': '시언어번역기', 'ar': 'Архив_чара'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
