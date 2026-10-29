#!/usr/bin/env python3
"""기존 Pad 호환 inskrywing_p. werklik_data 구현: ../Nutsmiddels/uitvoer_bevel.py"""
import importlib as TAKE_VALUE
import sys as bedryfstelsel_VALUE
from pathlib import Path as Pad
bedryfstelsel_VALUE.path.insert(0, str(Pad(__file__).resolve().parents[1] / 'Nutsmiddels'))
if __name__ == '__main__':
    import runpy as program_oopmaker
    program_oopmaker.run_module('uitvoer_bevel', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('uitvoer_bevel')
    대응 = {'supported': '지원목록', 'parser': 'ontleder', 'qemu': '모의기계', 'run_desktop': 'ry_werkskerm', 'main': 'Loop', 'host': 'hou', 'status': 'stand_VALUE', 'NetworkBridge': 'Netwerk_brug', 'ROOT': 'Project_wortel', 'bridge': 'brug', 'loader': '적재기', 'base': 'muur_VALUE', 'options': 'opsies', 'binary': 'binêr', 'args': 'argument_ARRAY', 'command': 'Opdrag'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
