#!/usr/bin/env python3
"""기존 Wee 호환 Agab_Punkt. aktuell_Daten 구현: ../Tools/ausféieren_Befeel.py"""
import importlib as TAKE_VALUE
import sys as Betribssystem_VALUE
from pathlib import Path as Wee
Betribssystem_VALUE.path.insert(0, str(Wee(__file__).resolve().parents[1] / 'Tools'))
if __name__ == '__main__':
    import runpy as App_App_Beräich
    App_App_Beräich.run_module('ausféieren_Befeel', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('ausféieren_Befeel')
    대응 = {'supported': '지원목록', 'parser': '인수해석기', 'qemu': '모의기계', 'run_desktop': 'Laf_Desktop', 'main': 'Laf', 'host': 'Host', 'status': 'Status_VALUE', 'NetworkBridge': 'Reseau_Bréck', 'ROOT': 'projezéieren_Racinn', 'bridge': 'Bréck', 'loader': '적재기', 'base': 'Hannergrond_VALUE', 'options': 'Optiounen', 'binary': 'Binär', 'args': 'Argument_ARRAY', 'command': 'Befeel'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
