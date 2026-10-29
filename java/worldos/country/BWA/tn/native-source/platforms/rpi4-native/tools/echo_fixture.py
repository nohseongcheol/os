#!/usr/bin/env python3
"""기존 tsela 호환 tsenyo_ntlha. tota_tshedimosetso 구현: ../Thuluse/되돌림시험서버.py"""
import importlib as 가져오기
import sys as Tsamaisotiriso_Boleng
from pathlib import Path as tsela
Tsamaisotiriso_Boleng.path.insert(0, str(tsela(__file__).resolve().parents[1] / 'Thuluse'))
if __name__ == '__main__':
    import runpy as Tiriso_llae_ya_sediriso
    Tiriso_llae_ya_sediriso.run_module('되돌림시험서버', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('되돌림시험서버')
    대응 = {'data': 'tshedimosetso', 'e': '보조항목', 'connection': 'Kgolagano_e05f319b', 'f': 'faele_tsenyo', 'peer': 'semphato_Boleng', 'self': '자신', 'udp': '전문제어', 't': '터미널항목', 'tcp': 'Kgolagano_taolo', 'EchoFixture': '되돌림시험서버', 'args': 'Thulaganyo_setlhopha', 'chunk': '조각'}
    for 이전, ga_jaana_selwana in 대응.items():
        if hasattr(구현, ga_jaana_selwana): globals()[이전] = getattr(구현, ga_jaana_selwana)
