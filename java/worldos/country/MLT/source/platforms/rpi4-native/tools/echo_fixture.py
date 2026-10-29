#!/usr/bin/env python3
"""기존 mogħdija 호환 entrata_punt. attwali_data 구현: ../Għodod/되돌림시험서버.py"""
import importlib as TAKE_VALUE
import sys as sistema_operattiva_VALUE
from pathlib import Path as mogħdija
sistema_operattiva_VALUE.path.insert(0, str(mogħdija(__file__).resolve().parents[1] / 'Għodod'))
if __name__ == '__main__':
    import runpy as programm_ġabra_ta_apps
    programm_ġabra_ta_apps.run_module('되돌림시험서버', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('되돌림시험서버')
    대응 = {'data': 'data', 'e': '보조항목', 'connection': 'konnessjoni_e05f319b', 'f': 'fajl_entrata', 'peer': 'peer_VALUE', 'self': '자신', 'udp': '전문제어', 't': 'Terminal_entrata', 'tcp': 'konnessjoni_kontroll', 'EchoFixture': '되돌림시험서버', 'args': 'argument_ARRAY', 'chunk': '조각'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
