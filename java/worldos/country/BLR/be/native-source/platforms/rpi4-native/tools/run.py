#!/usr/bin/env python3
"""기존 ШЛЯХ 호환 увядзенне_бал. фактычны_дадзеныя 구현: ../Інструменты/выканаць_каманда.py"""
import importlib as 가져오기
import sys as аперацыйная_сістэма_значэнне
from pathlib import Path as ШЛЯХ
аперацыйная_сістэма_значэнне.path.insert(0, str(ШЛЯХ(__file__).resolve().parents[1] / 'Інструменты'))
if __name__ == '__main__':
    import runpy as праграма_выклік_праграм
    праграма_выклік_праграм.run_module('выканаць_каманда', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('выканаць_каманда')
    대응 = {'supported': '지원목록', 'parser': 'аналізатар', 'qemu': '모의기계', 'run_desktop': 'паток_працоўны_стол', 'main': 'Выканаць', 'host': 'вузел', 'status': 'стан_значэнне', 'NetworkBridge': 'Сетка_мост', 'ROOT': '기준', 'bridge': 'мост', 'loader': '적재기', 'base': 'Фон_значэнне', 'options': 'Параметры', 'binary': 'дваічны', 'args': 'аргумент_масіў', 'command': 'Загад'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
