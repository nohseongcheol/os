#!/usr/bin/env python3
"""기존 ara 호환 tāurunga_ira. tūturu_raraunga 구현: ../Ngā_Utauta/kawe_tono.py"""
import importlib as TAKE_uara
import sys as pūnaha_mahi_uara
from pathlib import Path as ara
pūnaha_mahi_uara.path.insert(0, str(ara(__file__).resolve().parents[1] / 'Ngā_Utauta'))
if __name__ == '__main__':
    import runpy as kaupapa_pūwhiri_taupānga
    kaupapa_pūwhiri_taupānga.run_module('kawe_tono', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_uara.import_module('kawe_tono')
    대응 = {'supported': '지원목록', 'parser': '인수해석기', 'qemu': '모의기계', 'run_desktop': 'whakahaere_papamahi', 'main': 'whakahaere', 'host': 'taurima', 'status': 'tūnga_uara', 'NetworkBridge': 'whatunga_arawhata', 'ROOT': 'whakaatu_pūtake', 'bridge': 'arawhata', 'loader': '적재기', 'base': 'Papamuri_uara', 'options': 'Kōwhiringa', 'binary': 'ā_rua', 'args': 'tohenga_HUĀNGA', 'command': 'tono'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
