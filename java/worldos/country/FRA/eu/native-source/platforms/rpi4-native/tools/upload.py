#!/usr/bin/env python3
"""기존 Bide_izena 호환 sarrera_p. benetako_datuak 구현: ../Tresnak/Upload_Fitxategiak.py"""
import importlib as HARTU_balio
import sys as sistema_eragile_balio
from pathlib import Path as Bide_izena
sistema_eragile_balio.path.insert(0, str(Bide_izena(__file__).resolve().parents[1] / 'Tresnak'))
if __name__ == '__main__':
    import runpy as aplik_abiarazle
    aplik_abiarazle.run_module('Upload_Fitxategiak', run_name='__main__', alter_sys=True)
else:
    구현 = HARTU_balio.import_module('Upload_Fitxategiak')
    대응 = {'data': 'datuak', 'i': '순번', 'name': 'Izena', 'c': 'karaktere_kode', 'p': 'datuak_kargu', 'args': 'arg_matrize'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
