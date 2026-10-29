#!/usr/bin/env python3
"""기존 CEĻŠ 호환 ieejas_punkts. faktisks_dati 구현: ../Rīki/실행파일시험.py"""
import importlib as TAKE_VALUE
import sys as operētājsistēma_VALUE
from pathlib import Path as CEĻŠ
operētājsistēma_VALUE.path.insert(0, str(CEĻŠ(__file__).resolve().parents[1] / 'Rīki'))
if __name__ == '__main__':
    import runpy as programma_palaidējs
    programma_palaidējs.run_module('실행파일시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('실행파일시험')
    kartēšana_VALUE = {'out': 'mērs_dati', 'expected': '예상결과', 'phoff': 'programma_galvene_Nobīde', 'offset': 'Nobīde_VALUE', 'invalid': 'nederīgs_dati', 'path': 'CEĻŠ', 'executable': 'izpildāms_fails_IMAGE', 'rejected': '거부결과', 'linux_example': '리눅스예제', 'original': '원본', 'result': 'mērs', 'format_': 'formāts_b87fd068', 'main': 'Palaist', 'content': 'Saturs_VALUE', 'source': '원본자료', 'name': 'Nosaukums', 'reference': 'Salīdzinājums_bāze', 'ROOT': 'Project_sakne', 'value': 'VALUE', 'report': 'validācija_ziņot'}
    for 이전, pašreizējais_krājums in kartēšana_VALUE.items():
        if hasattr(구현, pašreizējais_krājums): globals()[이전] = getattr(구현, pašreizējais_krājums)
