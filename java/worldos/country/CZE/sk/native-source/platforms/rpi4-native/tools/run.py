#!/usr/bin/env python3
"""기존 Cesta 호환 položka_bod. skutočný_údaje 구현: ../Nástroje/Vykonať_príkaz.py"""
import importlib as TAKE_VALUE
import sys as operačný_systém_VALUE
from pathlib import Path as Cesta
operačný_systém_VALUE.path.insert(0, str(Cesta(__file__).resolve().parents[1] / 'Nástroje'))
if __name__ == '__main__':
    import runpy as program_spúšťač
    program_spúšťač.run_module('Vykonať_príkaz', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('Vykonať_príkaz')
    mapovanie_VALUE = {'supported': '지원목록', 'parser': 'analyzátor', 'qemu': '모의기계', 'run_desktop': 'spustiť_počítač', 'main': 'Spustiť_2', 'host': 'hostiteľ', 'status': 'Stav_VALUE', 'NetworkBridge': 'sieťový_most', 'ROOT': 'akcia_koreň', 'bridge': 'most', 'loader': 'zavádzací_program', 'base': 'tapeta_VALUE', 'options': 'Možnosti', 'binary': 'Binary', 'args': 'argument_pole', 'command': 'Príkaz'}
    for 이전, v_termíne_splatnosti_položka in mapovanie_VALUE.items():
        if hasattr(구현, v_termíne_splatnosti_položka): globals()[이전] = getattr(구현, v_termíne_splatnosti_položka)
