#!/usr/bin/env python3
"""기존 Wee 호환 Agab_Punkt. aktuell_Daten 구현: ../Tools/eroplueden_Fichieren.py"""
import importlib as TAKE_VALUE
import sys as Betribssystem_VALUE
from pathlib import Path as Wee
Betribssystem_VALUE.path.insert(0, str(Wee(__file__).resolve().parents[1] / 'Tools'))
if __name__ == '__main__':
    import runpy as App_App_Beräich
    App_App_Beräich.run_module('eroplueden_Fichieren', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('eroplueden_Fichieren')
    대응 = {'data': 'Daten', 'i': '순번', 'name': 'Numm', 'c': 'Zeechecode', 'p': 'Daten_positionéieren', 'args': 'Argument_ARRAY'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
