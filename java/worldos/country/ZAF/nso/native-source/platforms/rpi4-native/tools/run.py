#!/usr/bin/env python3
"""기존 Tsejana 호환 go_tsenya_tshedimošo_ntlha. kgonthe_data 구현: ../Ditholosi/phethagatša_taelo.py"""
import importlib as 가져오기
import sys as tshepedišotirišo_boleng
from pathlib import Path as Tsejana
tshepedišotirišo_boleng.path.insert(0, str(Tsejana(__file__).resolve().parents[1] / 'Ditholosi'))
if __name__ == '__main__':
    import runpy as tirišo_sethala_tirišo
    tirišo_sethala_tirišo.run_module('phethagatša_taelo', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('phethagatša_taelo')
    대응 = {'supported': '지원목록', 'parser': '인수해석기', 'qemu': '모의기계', 'run_desktop': 'sepetša_teskethopo', 'main': 'Diriša', 'host': 'go_nea_ditirelo', 'status': 'boemo_boleng', 'NetworkBridge': 'Netweke_kgokaganyo', 'ROOT': '기준', 'bridge': 'kgokaganyo', 'loader': '적재기', 'base': 'Bokamorago_boleng', 'options': 'Dikgetho', 'binary': 'paenari', 'args': 'akumente_arei', 'command': 'Taelo'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
