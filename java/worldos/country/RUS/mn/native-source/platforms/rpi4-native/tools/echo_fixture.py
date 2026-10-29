#!/usr/bin/env python3
"""기존 ЗАМ 호환 оролт_цэг. бодит_өгөгдөл 구현: ../Хэрэгслүүд/되돌림시험서버.py"""
import importlib as 가져오기
import sys as үйлдлийн_систем_утга
from pathlib import Path as ЗАМ
үйлдлийн_систем_утга.path.insert(0, str(ЗАМ(__file__).resolve().parents[1] / 'Хэрэгслүүд'))
if __name__ == '__main__':
    import runpy as програм_гишүүн
    програм_гишүүн.run_module('되돌림시험서버', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('되돌림시험서버')
    대응 = {'data': 'өгөгдөл', 'e': '보조항목', 'connection': 'холболт_e05f319b', 'f': 'файл_оролт', 'peer': 'ижил_түвшин_утга', 'self': '자신', 'udp': '전문제어', 't': '터미널항목', 'tcp': 'холболт_хяналт', 'EchoFixture': '되돌림시험서버', 'args': 'аргумент_олонлог', 'chunk': '조각'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
