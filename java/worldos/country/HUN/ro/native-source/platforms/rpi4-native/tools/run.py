#!/usr/bin/env python3
"""기존 Cale 호환 intrare_p. real_date 구현: ../Instrumente/executa_comandă.py"""
import importlib as TAKE_VALUE
import sys as sistem_de_operare_VALUE
from pathlib import Path as Cale
sistem_de_operare_VALUE.path.insert(0, str(Cale(__file__).resolve().parents[1] / 'Instrumente'))
if __name__ == '__main__':
    import runpy as program_ecrane_de_lansare
    program_ecrane_de_lansare.run_module('executa_comandă', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('executa_comandă')
    mapare_VALUE = {'supported': '지원목록', 'parser': 'parser', 'qemu': '모의기계', 'run_desktop': 'rula_desktop', 'main': 'Pornește', 'host': 'gazdă', 'status': 'Stare_VALUE', 'NetworkBridge': 'punte_3de4fe3a', 'ROOT': 'Project_rădăcină', 'bridge': 'punte', 'loader': 'încărcător', 'base': 'tapet_VALUE', 'options': 'Opțiuni', 'binary': 'binar', 'args': 'argument_ARRAY', 'command': 'Comandă'}
    for Anteriorul_element, curent_element in mapare_VALUE.items():
        if hasattr(구현, curent_element): globals()[Anteriorul_element] = getattr(구현, curent_element)
