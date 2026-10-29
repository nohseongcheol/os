#!/usr/bin/env python3
"""기존 Inzira 호환 icyinjizwa_inota. nyakuri_amakurushingiro 구현: ../Ibikoresho/gukora_ibwiriza.py"""
import importlib as 가져오기
import sys as sisitemu_ngengamikorere_agaciro
from pathlib import Path as Inzira
sisitemu_ngengamikorere_agaciro.path.insert(0, str(Inzira(__file__).resolve().parents[1] / 'Ibikoresho'))
if __name__ == '__main__':
    import runpy as porogaramu_umukozi
    porogaramu_umukozi.run_module('gukora_ibwiriza', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('gukora_ibwiriza')
    대응 = {'supported': '지원목록', 'parser': '인수해석기', 'qemu': '모의기계', 'run_desktop': 'ihuriro_biro', 'main': 'ihuriro', 'host': 'gucumbikira', 'status': 'imimerere_agaciro', 'NetworkBridge': '통신다리', 'ROOT': '기준', 'bridge': '연결다리', 'loader': '적재기', 'base': 'Imbuganyuma_agaciro', 'options': 'Amahitamo', 'binary': 'nyabibiri', 'args': 'ingingo_ARRAY', 'command': 'Icyo_wifuza'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
