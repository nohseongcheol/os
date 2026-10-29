#!/usr/bin/env python3
"""기존 ЗАМ 호환 оролт_цэг. бодит_өгөгдөл 구현: ../Хэрэгслүүд/байршуулах_Файлууд.py"""
import importlib as 가져오기
import sys as үйлдлийн_систем_утга
from pathlib import Path as ЗАМ
үйлдлийн_систем_утга.path.insert(0, str(ЗАМ(__file__).resolve().parents[1] / 'Хэрэгслүүд'))
if __name__ == '__main__':
    import runpy as програм_гишүүн
    програм_гишүүн.run_module('байршуулах_Файлууд', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('байршуулах_Файлууд')
    대응 = {'data': 'өгөгдөл', 'i': '순번', 'name': 'Нэр', 'c': 'тэмдэгтийн_код', 'p': '자료위치', 'args': 'аргумент_олонлог'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
