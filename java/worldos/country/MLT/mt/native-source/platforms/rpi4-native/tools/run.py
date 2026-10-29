#!/usr/bin/env python3
"""기존 mogħdija 호환 entrata_punt. attwali_data 구현: ../Għodod/eżegwixxa_kmand.py"""
import importlib as TAKE_VALUE
import sys as sistema_operattiva_VALUE
from pathlib import Path as mogħdija
sistema_operattiva_VALUE.path.insert(0, str(mogħdija(__file__).resolve().parents[1] / 'Għodod'))
if __name__ == '__main__':
    import runpy as programm_ġabra_ta_apps
    programm_ġabra_ta_apps.run_module('eżegwixxa_kmand', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('eżegwixxa_kmand')
    대응 = {'supported': '지원목록', 'parser': '인수해석기', 'qemu': '모의기계', 'run_desktop': 'serje_desktop', 'main': 'serje', 'host': 'host', 'status': 'stat_VALUE', 'NetworkBridge': 'netwerk_pont', 'ROOT': 'pprojetta_għerq', 'bridge': 'pont', 'loader': '적재기', 'base': 'Sfond_VALUE', 'options': 'Għażliet', 'binary': 'binarju', 'args': 'argument_ARRAY', 'command': 'kmand'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
