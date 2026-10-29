#!/usr/bin/env python3
"""기존 ЖОЛ 호환 киргизме_жазуу_упай. актуалдуу_берилмелер 구현: ../Куралдар/жүктөп_жөнөтүү_Файлдар.py"""
import importlib as 가져오기
import sys as оперативдик_система_маани
from pathlib import Path as ЖОЛ
оперативдик_система_маани.path.insert(0, str(ЖОЛ(__file__).resolve().parents[1] / 'Куралдар'))
if __name__ == '__main__':
    import runpy as програм_жаратма_тарткычы
    програм_жаратма_тарткычы.run_module('жүктөп_жөнөтүү_Файлдар', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('жүктөп_жөнөтүү_Файлдар')
    대응 = {'data': 'берилмелер', 'i': '순번', 'name': 'Аты', 'c': 'символ_коду', 'p': '자료위치', 'args': 'аргумент_МАССИВ'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
