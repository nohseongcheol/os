#!/usr/bin/env python3
"""기존 Жол_2 호환 енгізу_ұпай. нақты_деректер 구현: ../Құралдар/되돌림시험서버.py"""
import importlib as 가져오기
import sys as операциялық_жүйе_мән
from pathlib import Path as Жол_2
операциялық_жүйе_мән.path.insert(0, str(Жол_2(__file__).resolve().parents[1] / 'Құралдар'))
if __name__ == '__main__':
    import runpy as бағдарлама_іске_қосу_құралы
    бағдарлама_іске_қосу_құралы.run_module('되돌림시험서버', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('되돌림시험서버')
    대응 = {'data': 'деректер', 'e': '보조항목', 'connection': 'қосылым_e05f319b', 'f': 'файл_енгізу', 'peer': 'бір_рангілі_мән', 'self': '자신', 'udp': '전문제어', 't': 'Терминал_енгізу', 'tcp': 'қосылым_Басқару', 'EchoFixture': '되돌림시험서버', 'args': 'аргумент_массив', 'chunk': '조각'}
    for 이전, ток_элемент in 대응.items():
        if hasattr(구현, ток_элемент): globals()[이전] = getattr(구현, ток_элемент)
