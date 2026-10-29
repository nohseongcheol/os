#!/usr/bin/env python3
"""기존 Bide_izena 호환 sarrera_p. benetako_datuak 구현: ../Tresnak/개발꾸러미번역.py"""
import importlib as HARTU_balio
import sys as sistema_eragile_balio
from pathlib import Path as Bide_izena
sistema_eragile_balio.path.insert(0, str(Bide_izena(__file__).resolve().parents[1] / 'Tresnak'))
if __name__ == '__main__':
    import runpy as aplik_abiarazle
    aplik_abiarazle.run_module('개발꾸러미번역', run_name='__main__', alter_sys=True)
else:
    구현 = HARTU_balio.import_module('개발꾸러미번역')
    대응 = {'compiler': '번역기', 'obj': 'helburuko_fitxategi', 'sdk': '개발꾸러미', 'output': '출력결과', 'main': 'Exekutatu_2', 'elf': '실행파일', 'is_c': '시언어여부', 'parser': 'analizatzaile', 'language': 'Hizkuntza', 'work': '작업경로', 'args': 'arg_matrize'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
