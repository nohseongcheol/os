#!/usr/bin/env python3
"""기존 ara 호환 tāurunga_ira. tūturu_raraunga 구현: ../Ngā_Utauta/흐름시험.py"""
import importlib as TAKE_uara
import sys as pūnaha_mahi_uara
from pathlib import Path as ara
pūnaha_mahi_uara.path.insert(0, str(ara(__file__).resolve().parents[1] / 'Ngā_Utauta'))
if __name__ == '__main__':
    import runpy as kaupapa_pūwhiri_taupānga
    kaupapa_pūwhiri_taupānga.run_module('흐름시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_uara.import_module('흐름시험')
    대응 = {'out': 'mēhua_raraunga', 'main': 'whakahaere', 'ROOT': 'whakaatu_pūtake', 'p': 'raraunga_tūranga', 'text': 'Ngā_kupu', 'report': 'whakamana_pūrongo'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
