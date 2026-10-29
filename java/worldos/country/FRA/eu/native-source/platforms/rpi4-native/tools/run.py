#!/usr/bin/env python3
"""기존 Bide_izena 호환 sarrera_p. benetako_datuak 구현: ../Tresnak/exekutatu_komando.py"""
import importlib as HARTU_balio
import sys as sistema_eragile_balio
from pathlib import Path as Bide_izena
sistema_eragile_balio.path.insert(0, str(Bide_izena(__file__).resolve().parents[1] / 'Tresnak'))
if __name__ == '__main__':
    import runpy as aplik_abiarazle
    aplik_abiarazle.run_module('exekutatu_komando', run_name='__main__', alter_sys=True)
else:
    구현 = HARTU_balio.import_module('exekutatu_komando')
    대응 = {'supported': '지원목록', 'parser': 'analizatzaile', 'qemu': '모의기계', 'run_desktop': 'exekutatu_mahaigain', 'main': 'Exekutatu_2', 'host': 'Ostalari', 'status': 'Egoera_balio', 'NetworkBridge': 'sare_zubi', 'ROOT': 'Project_erro', 'bridge': 'zubi', 'loader': '적재기', 'base': 'horma_paper_balio', 'options': 'aukerak', 'binary': 'bitar', 'args': 'arg_matrize', 'command': 'Komandoa'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
