#!/usr/bin/env python3
"""기존 CEĻŠ 호환 ieejas_punkts. faktisks_dati 구현: ../Rīki/būvējums_tīkls.py"""
import importlib as TAKE_VALUE
import sys as operētājsistēma_VALUE
from pathlib import Path as CEĻŠ
operētājsistēma_VALUE.path.insert(0, str(CEĻŠ(__file__).resolve().parents[1] / 'Rīki'))
if __name__ == '__main__':
    import runpy as programma_palaidējs
    programma_palaidējs.run_module('būvējums_tīkls', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('būvējums_tīkls')
    kartēšana_VALUE = {'obj': 'mērķa_fails', 'objects': 'mērķis_Faili', 'library': 'bibliotēka', 'output': 'ražojums', 'port': 'porta_numurs', 'root': 'sakne_adrese', 'files': 'Fails_Saraksts', 'source': '원본자료', 'run': 'Izpildīt_komanda', 'flags': 'konfigurācija_Background_Intelligent_Transfer_Service', 'path': 'CEĻŠ', 'build_network': 'atvērt_tīkls_48d29d6d', 'cc': 'C_kompilators', 'ar': 'Arhīvs_rīks'}
    for 이전, pašreizējais_krājums in kartēšana_VALUE.items():
        if hasattr(구현, pašreizējais_krājums): globals()[이전] = getattr(구현, pašreizējais_krājums)
