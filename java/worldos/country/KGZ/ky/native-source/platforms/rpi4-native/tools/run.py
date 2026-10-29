#!/usr/bin/env python3
"""기존 ЖОЛ 호환 киргизме_жазуу_упай. актуалдуу_берилмелер 구현: ../Куралдар/аткаруу_буйрук.py"""
import importlib as 가져오기
import sys as оперативдик_система_маани
from pathlib import Path as ЖОЛ
оперативдик_система_маани.path.insert(0, str(ЖОЛ(__file__).resolve().parents[1] / 'Куралдар'))
if __name__ == '__main__':
    import runpy as програм_жаратма_тарткычы
    програм_жаратма_тарткычы.run_module('аткаруу_буйрук', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('аткаруу_буйрук')
    대응 = {'supported': '지원목록', 'parser': '인수해석기', 'qemu': '모의기계', 'run_desktop': 'топтом_иш_такта', 'main': 'Жүргүзүү', 'host': 'кабылдоо', 'status': 'абал_маани', 'NetworkBridge': '통신다리', 'ROOT': '기준', 'bridge': '연결다리', 'loader': '적재기', 'base': 'Фон_маани', 'options': 'Параметрлер', 'binary': 'экилик', 'args': 'аргумент_МАССИВ', 'command': 'Команда'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
