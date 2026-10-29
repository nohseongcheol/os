#!/usr/bin/env python3
"""기존 CEĻŠ 호환 ieejas_punkts. faktisks_dati 구현: ../Rīki/atvērt_IMAGE.py"""
import importlib as TAKE_VALUE
import sys as operētājsistēma_VALUE
from pathlib import Path as CEĻŠ
operētājsistēma_VALUE.path.insert(0, str(CEĻŠ(__file__).resolve().parents[1] / 'Rīki'))
if __name__ == '__main__':
    import runpy as programma_palaidējs
    programma_palaidējs.run_module('atvērt_IMAGE', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('atvērt_IMAGE')
    kartēšana_VALUE = {'total': 'kopsumma_noslodze', 'start': 'Palaist', 'firmware': 'aparātprogrammatūra_VALUE', 'files': 'Fails_Saraksts', 'archive_base': 'Arhīvs_BASE', 'partition': 'nodalījums_Fails', 'archive': 'Arhīvs', 'main': 'Palaist', 'block': 'datu_bloks', 'ROOT': 'Project_sakne', 'boot': '부팅경로', 'stage': 'posms_VALUE', 'out': 'mērs_dati', 'expected': '예상결과', 'f': 'Fails_ievade', 'src': '원본주소', 'path': 'CEĻŠ', 'p': 'dati_amats', 'extracted': '추출자료', 'member': 'elements', 'mbr': 'MBR', 'image': 'IMAGE', 'sector_count': '섹터개수', 'dist': 'sadale_ceļš', 'sha': '해시계산', 'license_': 'licence', 'source': '원본자료', 'name': 'Nosaukums', 'value': 'VALUE', 'manifest': '꾸러미명세', 'dest': 'mērķis_VALUE_amats', 'work': '작업경로'}
    for 이전, pašreizējais_krājums in kartēšana_VALUE.items():
        if hasattr(구현, pašreizējais_krājums): globals()[이전] = getattr(구현, pašreizējais_krājums)
