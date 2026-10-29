#!/usr/bin/env python3
"""기존 Bide_izena 호환 sarrera_p. benetako_datuak 구현: ../Tresnak/흐름시험.py"""
import importlib as HARTU_balio
import sys as sistema_eragile_balio
from pathlib import Path as Bide_izena
sistema_eragile_balio.path.insert(0, str(Bide_izena(__file__).resolve().parents[1] / 'Tresnak'))
if __name__ == '__main__':
    import runpy as aplik_abiarazle
    aplik_abiarazle.run_module('흐름시험', run_name='__main__', alter_sys=True)
else:
    구현 = HARTU_balio.import_module('흐름시험')
    대응 = {'out': 'neurria_datuak', 'main': 'Exekutatu_2', 'ROOT': 'Project_erro', 'p': 'datuak_kargu', 'text': 'Testua', 'report': 'balidazio_txosten'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
