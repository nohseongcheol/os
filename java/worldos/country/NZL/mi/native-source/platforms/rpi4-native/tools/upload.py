#!/usr/bin/env python3
"""기존 ara 호환 tāurunga_ira. tūturu_raraunga 구현: ../Ngā_Utauta/tukuatu_Ngā_Kōnae.py"""
import importlib as TAKE_uara
import sys as pūnaha_mahi_uara
from pathlib import Path as ara
pūnaha_mahi_uara.path.insert(0, str(ara(__file__).resolve().parents[1] / 'Ngā_Utauta'))
if __name__ == '__main__':
    import runpy as kaupapa_pūwhiri_taupānga
    kaupapa_pūwhiri_taupānga.run_module('tukuatu_Ngā_Kōnae', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_uara.import_module('tukuatu_Ngā_Kōnae')
    대응 = {'data': 'raraunga', 'i': '순번', 'name': 'Ingoa', 'c': 'waehere_pūāhua', 'p': 'raraunga_tūranga', 'args': 'tohenga_HUĀNGA'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
