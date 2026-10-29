#!/usr/bin/env python3
"""기존 LLWYBR 호환 cofnod_p. go_iawn_data 구현: ../Offer/Gweithredu_gorchymyn.py"""
import importlib as TAKE_VALUE
import sys as system_weithredu_VALUE
from pathlib import Path as LLWYBR
system_weithredu_VALUE.path.insert(0, str(LLWYBR(__file__).resolve().parents[1] / 'Offer'))
if __name__ == '__main__':
    import runpy as Rhaglen_lansiwr
    Rhaglen_lansiwr.run_module('Gweithredu_gorchymyn', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('Gweithredu_gorchymyn')
    대응 = {'supported': '지원목록', 'parser': '인수해석기', 'qemu': '모의기계', 'run_desktop': 'rhedeg_bwrdd_gwaith', 'main': 'Gweithredu_2', 'host': 'lletya', 'status': 'cyflwr_VALUE', 'NetworkBridge': 'Rhwydwaith_pont', 'ROOT': 'prosiect_gwraidd', 'bridge': 'pont', 'loader': '적재기', 'base': 'Cefndir_VALUE', 'options': 'Dewisiadau', 'binary': 'deuaidd', 'args': 'arg_ARAE', 'command': 'Gorchymyn'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
