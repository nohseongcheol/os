#!/usr/bin/env python3
"""기존 Yul 호환 кертү_балл. фактик_мәгълүмат 구현: ../Кораллар/төзү_PYTHON.py"""
import importlib as TAKE_VALUE
import sys as операцион_система_VALUE
from pathlib import Path as Yul
операцион_система_VALUE.path.insert(0, str(Yul(__file__).resolve().parents[1] / 'Кораллар'))
if __name__ == '__main__':
    import runpy as кушымта_хезмәткәр
    кушымта_хезмәткәр.run_module('төзү_PYTHON', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('төзү_PYTHON')
    대응 = {'ld': '연결편집기', 'archive': 'Архив', 'SHA256': 'раслау_Хәш', 'build_python': 'Төзү_PYTHON', 'root': 'тамыр_адрес', 'source': '원본자료', 'name': 'исем', 'path': 'Yul', 'VERSION': '배포판', 'cc': '시언어번역기', 'tar': '타르꾸러미', 'newlib': '뉴리브포함경로', 'member': 'бүлек'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
