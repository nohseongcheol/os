#!/usr/bin/env python3
"""기존 ШЛЯХ 호환 увядзенне_бал. фактычны_дадзеныя 구현: ../Інструменты/запампоўка_Файлы.py"""
import importlib as 가져오기
import sys as аперацыйная_сістэма_значэнне
from pathlib import Path as ШЛЯХ
аперацыйная_сістэма_значэнне.path.insert(0, str(ШЛЯХ(__file__).resolve().parents[1] / 'Інструменты'))
if __name__ == '__main__':
    import runpy as праграма_выклік_праграм
    праграма_выклік_праграм.run_module('запампоўка_Файлы', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('запампоўка_Файлы')
    대응 = {'data': 'дадзеныя', 'i': '순번', 'name': 'Назва', 'c': 'код_сімвала', 'p': '자료위치', 'args': 'аргумент_масіў'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
