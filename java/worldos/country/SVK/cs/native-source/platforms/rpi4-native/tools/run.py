#!/usr/bin/env python3
"""기존 cesta_2 호환 vstupní_bod. skutečný_data implementace: ../nástroje/Provést_příkaz.py"""
import importlib as VZÍT_HODNOTA
import sys as operační_systém_HODNOTA
from pathlib import Path as cesta_2
operační_systém_HODNOTA.path.insert(0, str(cesta_2(__file__).resolve().parents[1] / 'nástroje'))
if __name__ == '__main__':
    import runpy as program_Launcher
    program_Launcher.run_module('Provést_příkaz', run_name='__main__', alter_sys=True)
else:
    implementace = VZÍT_HODNOTA.import_module('Provést_příkaz')
    대응 = {'supported': '지원목록', 'parser': 'analyzátor', 'qemu': '모의기계', 'run_desktop': 'spustit_Plocha', 'main': 'Spustit_2', 'host': 'hostit', 'status': 'Stav_HODNOTA', 'NetworkBridge': 'most_3de4fe3a', 'ROOT': 'akce_kořen', 'bridge': 'most', 'loader': 'zavaděč', 'base': 'Pozadí_HODNOTA', 'options': 'Možnosti', 'binary': 'binary', 'args': 'argument_pole', 'command': 'příkaz'}
    for Předchozí_zboží, dobrá_zboží in 대응.items():
        if hasattr(implementace, dobrá_zboží): globals()[Předchozí_zboží] = getattr(implementace, dobrá_zboží)
