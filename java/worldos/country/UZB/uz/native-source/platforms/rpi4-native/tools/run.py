#!/usr/bin/env python3
"""기존 yo_l 호환 kiritish_nuqta. real_ma_lumotlar 구현: ../Vositalar/bajarmoq_buyruq.py"""
import importlib as TAKE_VALUE
import sys as operatsion_tizim_VALUE
from pathlib import Path as yo_l
operatsion_tizim_VALUE.path.insert(0, str(yo_l(__file__).resolve().parents[1] / 'Vositalar'))
if __name__ == '__main__':
    import runpy as ilova_ilovalar_paneli
    ilova_ilovalar_paneli.run_module('bajarmoq_buyruq', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('bajarmoq_buyruq')
    대응 = {'supported': '지원목록', 'parser': 'parser', 'qemu': '모의기계', 'run_desktop': 'ishlash_ishchi_stol', 'main': 'Bajarish', 'host': 'tashkilotchi', 'status': 'holat_VALUE_e10195a1', 'NetworkBridge': '통신다리', 'ROOT': 'Project_ildiz', 'bridge': '연결다리', 'loader': '적재기', 'base': 'Fon_VALUE', 'options': 'Opsiyalar', 'binary': 'binar', 'args': 'dalil_ARRAY', 'command': 'Buyruq'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
