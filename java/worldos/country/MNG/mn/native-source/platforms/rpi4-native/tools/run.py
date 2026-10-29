#!/usr/bin/env python3
"""기존 ЗАМ 호환 оролт_цэг. бодит_өгөгдөл 구현: ../Хэрэгслүүд/Гүйцэтгэх_команд.py"""
import importlib as 가져오기
import sys as үйлдлийн_систем_утга
from pathlib import Path as ЗАМ
үйлдлийн_систем_утга.path.insert(0, str(ЗАМ(__file__).resolve().parents[1] / 'Хэрэгслүүд'))
if __name__ == '__main__':
    import runpy as програм_гишүүн
    програм_гишүүн.run_module('Гүйцэтгэх_команд', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('Гүйцэтгэх_команд')
    대응 = {'supported': '지원목록', 'parser': '인수해석기', 'qemu': '모의기계', 'run_desktop': 'ажиллах_дэлгэц', 'main': 'Ажиллуулах', 'host': 'хост', 'status': 'төлөв_утга', 'NetworkBridge': '통신다리', 'ROOT': '기준', 'bridge': '연결다리', 'loader': '적재기', 'base': 'Дэвсгэр_утга', 'options': 'Сонголтууд', 'binary': 'хоёрт', 'args': 'аргумент_олонлог', 'command': 'Тушаал'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
