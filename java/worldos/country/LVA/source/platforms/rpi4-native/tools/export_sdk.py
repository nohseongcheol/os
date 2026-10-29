#!/usr/bin/env python3
"""기존 CEĻŠ 호환 ieejas_punkts. faktisks_dati 구현: ../Rīki/eksportēt_SDK.py"""
import importlib as TAKE_VALUE
import sys as operētājsistēma_VALUE
from pathlib import Path as CEĻŠ
operētājsistēma_VALUE.path.insert(0, str(CEĻŠ(__file__).resolve().parents[1] / 'Rīki'))
if __name__ == '__main__':
    import runpy as programma_palaidējs
    programma_palaidējs.run_module('eksportēt_SDK', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('eksportēt_SDK')
    kartēšana_VALUE = {'out': 'mērs_dati', 'obj': 'mērķa_fails', 'relative': 'relatīvais_ceļš', 'compiler_archive': 'kompilators_Arhīvs', 'sdk': 'programmizstrādes_komplekts', 'dist': 'sadale_ceļš', 'archive': 'Arhīvs', 'main': 'Palaist', 'posix': '포직스경로', 'files': 'Fails_Saraksts', 'source': '원본자료', 'name': 'Nosaukums', 'target': 'mērķis', 'ROOT': 'Project_sakne', 'destination': 'mērķis_dati_adrese', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, pašreizējais_krājums in kartēšana_VALUE.items():
        if hasattr(구현, pašreizējais_krājums): globals()[이전] = getattr(구현, pašreizējais_krājums)
