#!/usr/bin/env python3
"""기존 Inzira 호환 icyinjizwa_inota. nyakuri_amakurushingiro 구현: ../Ibikoresho/되돌림시험서버.py"""
import importlib as 가져오기
import sys as sisitemu_ngengamikorere_agaciro
from pathlib import Path as Inzira
sisitemu_ngengamikorere_agaciro.path.insert(0, str(Inzira(__file__).resolve().parents[1] / 'Ibikoresho'))
if __name__ == '__main__':
    import runpy as porogaramu_umukozi
    porogaramu_umukozi.run_module('되돌림시험서버', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('되돌림시험서버')
    대응 = {'data': 'amakurushingiro', 'e': '보조항목', 'connection': 'kwihuza_e05f319b', 'f': 'dosiye_icyinjizwa', 'peer': 'Mugenzi_agaciro', 'self': '자신', 'udp': '전문제어', 't': '터미널항목', 'tcp': 'kwihuza_icunga', 'EchoFixture': '되돌림시험서버', 'args': 'ingingo_ARRAY', 'chunk': '조각'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
