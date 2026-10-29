#!/usr/bin/env python3
"""기존 POZICIONI 호환 futje_p. aktual_të_dhëna 구현: ../Mjete/zbatoj_komandë.py"""
import importlib as TAKE_VALUE
import sys as sistem_operativ_VALUE
from pathlib import Path as POZICIONI
sistem_operativ_VALUE.path.insert(0, str(POZICIONI(__file__).resolve().parents[1] / 'Mjete'))
if __name__ == '__main__':
    import runpy as program_hapës
    program_hapës.run_module('zbatoj_komandë', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('zbatoj_komandë')
    대응 = {'supported': '지원목록', 'parser': 'analizues', 'qemu': '모의기계', 'run_desktop': 'varg_desktop', 'main': 'Ekzekuto', 'host': 'pritës', 'status': 'status_VALUE', 'NetworkBridge': 'rrjet_urë', 'ROOT': 'Project_rrënjë', 'bridge': 'urë', 'loader': '적재기', 'base': 'Sfond_VALUE', 'options': 'Opsione', 'binary': 'binar', 'args': 'argument_ARRAY', 'command': 'Komanda'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
