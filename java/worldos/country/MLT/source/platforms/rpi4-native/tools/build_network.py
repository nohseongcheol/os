#!/usr/bin/env python3
"""기존 mogħdija 호환 entrata_punt. attwali_data 구현: ../Għodod/bena_netwerk.py"""
import importlib as TAKE_VALUE
import sys as sistema_operattiva_VALUE
from pathlib import Path as mogħdija
sistema_operattiva_VALUE.path.insert(0, str(mogħdija(__file__).resolve().parents[1] / 'Għodod'))
if __name__ == '__main__':
    import runpy as programm_ġabra_ta_apps
    programm_ġabra_ta_apps.run_module('bena_netwerk', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('bena_netwerk')
    대응 = {'obj': 'fajl_tad_destinazzjoni', 'objects': 'destinazzjoni_Fajls', 'library': 'librerija', 'output': '출력결과', 'port': '접속번호', 'root': 'għerq_ADDRESS', 'files': 'fajl_Lista', 'source': '원본자료', 'run': 'eżegwixxa_kmand', 'flags': '설정비트', 'path': 'mogħdija', 'build_network': 'ħalaq_netwerk', 'cc': '시언어번역기', 'ar': 'Arkivju_għodda'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
