#!/usr/bin/env python3
"""기존 Bide_izena 호환 sarrera_p. benetako_datuak 구현: ../Tresnak/코딩시험.py"""
import importlib as HARTU_balio
import sys as sistema_eragile_balio
from pathlib import Path as Bide_izena
sistema_eragile_balio.path.insert(0, str(Bide_izena(__file__).resolve().parents[1] / 'Tresnak'))
if __name__ == '__main__':
    import runpy as aplik_abiarazle
    aplik_abiarazle.run_module('코딩시험', run_name='__main__', alter_sys=True)
else:
    구현 = HARTU_balio.import_module('코딩시험')
    대응 = {'out': 'neurria_datuak', 'expected': '예상결과', 'sdk': '개발꾸러미', 'suffix': '뒷부분', 'arc': '압축묶음', 'main': 'Exekutatu_2', 'elf': '실행파일', 'run': 'exekutatu_komando', 'name': 'Izena', 'path': 'Bide_izena', 'p': 'datuak_kargu', 'ROOT': 'Project_erro', 'report': 'balidazio_txosten', 'args': 'arg_matrize'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
