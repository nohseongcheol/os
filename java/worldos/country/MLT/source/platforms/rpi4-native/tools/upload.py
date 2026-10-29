#!/usr/bin/env python3
"""기존 mogħdija 호환 entrata_punt. attwali_data 구현: ../Għodod/tella_Fajls.py"""
import importlib as TAKE_VALUE
import sys as sistema_operattiva_VALUE
from pathlib import Path as mogħdija
sistema_operattiva_VALUE.path.insert(0, str(mogħdija(__file__).resolve().parents[1] / 'Għodod'))
if __name__ == '__main__':
    import runpy as programm_ġabra_ta_apps
    programm_ġabra_ta_apps.run_module('tella_Fajls', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('tella_Fajls')
    대응 = {'data': 'data', 'i': '순번', 'name': 'isem', 'c': 'kodiċi_tal_karattru', 'p': 'data_pożizzjoni', 'args': 'argument_ARRAY'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
