#!/usr/bin/env python3
"""기존 CEĻŠ 호환 ieejas_punkts. faktisks_dati 구현: ../Rīki/būvējums_PYTHON.py"""
import importlib as TAKE_VALUE
import sys as operētājsistēma_VALUE
from pathlib import Path as CEĻŠ
operētājsistēma_VALUE.path.insert(0, str(CEĻŠ(__file__).resolve().parents[1] / 'Rīki'))
if __name__ == '__main__':
    import runpy as programma_palaidējs
    programma_palaidējs.run_module('būvējums_PYTHON', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('būvējums_PYTHON')
    kartēšana_VALUE = {'ld': '연결편집기', 'archive': 'Arhīvs', 'SHA256': 'validācija_jaukšana', 'build_python': 'atvērt_PYTHON', 'root': 'sakne_adrese', 'source': '원본자료', 'name': 'Nosaukums', 'path': 'CEĻŠ', 'VERSION': 'izdevums_VALUE', 'cc': 'C_kompilators', 'tar': '타르꾸러미', 'newlib': '뉴리브포함경로', 'member': 'elements'}
    for 이전, pašreizējais_krājums in kartēšana_VALUE.items():
        if hasattr(구현, pašreizējais_krājums): globals()[이전] = getattr(구현, pašreizējais_krājums)
