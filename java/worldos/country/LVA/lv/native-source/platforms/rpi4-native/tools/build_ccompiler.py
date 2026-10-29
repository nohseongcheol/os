#!/usr/bin/env python3
"""기존 CEĻŠ 호환 ieejas_punkts. faktisks_dati 구현: ../Rīki/būvējums_C_kompilators.py"""
import importlib as TAKE_VALUE
import sys as operētājsistēma_VALUE
from pathlib import Path as CEĻŠ
operētājsistēma_VALUE.path.insert(0, str(CEĻŠ(__file__).resolve().parents[1] / 'Rīki'))
if __name__ == '__main__':
    import runpy as programma_palaidējs
    programma_palaidējs.run_module('būvējums_C_kompilators', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('būvējums_C_kompilators')
    kartēšana_VALUE = {'out': 'mērs_dati', 'builtins': '내장연산', 'header': 'galvene_VALUE', 'sdk': 'programmizstrādes_komplekts', 'build_ccompiler': 'atvērt_C_kompilators', 'i': '순번', 'elf': 'izpildāms_fails', 'run': 'Izpildīt_komanda', 'flags': 'konfigurācija_Background_Intelligent_Transfer_Service', 'path': 'CEĻŠ', 'p': 'dati_amats', 'cc': 'C_kompilators', 'obj': 'mērķa_fails', 'flag': 'Iestatījumi_VALUE', 'ld': '연결편집기', 'objects': 'mērķis_Faili', 'repo': 'repozitorijs_ceļš', 'v': '임시값', 'upstream': 'iepriekšējs', 'root': 'sakne_adrese', 'assets': '탑재자료', 'source': '원본자료', 'name': 'Nosaukums', 'includes': '포함인수'}
    for 이전, pašreizējais_krājums in kartēšana_VALUE.items():
        if hasattr(구현, pašreizējais_krājums): globals()[이전] = getattr(구현, pašreizējais_krājums)
