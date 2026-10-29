#!/usr/bin/env python3
"""기존 Жол_2 호환 енгізу_ұпай. нақты_деректер 구현: ../Құралдар/орындау_пәрмен.py"""
import importlib as 가져오기
import sys as операциялық_жүйе_мән
from pathlib import Path as Жол_2
операциялық_жүйе_мән.path.insert(0, str(Жол_2(__file__).resolve().parents[1] / 'Құралдар'))
if __name__ == '__main__':
    import runpy as бағдарлама_іске_қосу_құралы
    бағдарлама_іске_қосу_құралы.run_module('орындау_пәрмен', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('орындау_пәрмен')
    대응 = {'supported': '지원목록', 'parser': 'талдау_құралы', 'qemu': '모의기계', 'run_desktop': 'орындалу_үстелдік', 'main': 'Орындау_2', 'host': 'орналастыру', 'status': 'күй_мән', 'NetworkBridge': 'желі_көпір', 'ROOT': 'жоба_түбір', 'bridge': 'көпір', 'loader': '적재기', 'base': 'Фон_мән', 'options': 'Параметрлер', 'binary': 'екілік', 'args': 'аргумент_массив', 'command': 'Команда'}
    for 이전, ток_элемент in 대응.items():
        if hasattr(구현, ток_элемент): globals()[이전] = getattr(구현, ток_элемент)
