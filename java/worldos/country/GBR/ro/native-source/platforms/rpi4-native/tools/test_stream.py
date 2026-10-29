#!/usr/bin/env python3
"""기존 Cale 호환 intrare_p. real_date 구현: ../Instrumente/흐름시험.py"""
import importlib as TAKE_VALUE
import sys as sistem_de_operare_VALUE
from pathlib import Path as Cale
sistem_de_operare_VALUE.path.insert(0, str(Cale(__file__).resolve().parents[1] / 'Instrumente'))
if __name__ == '__main__':
    import runpy as program_ecrane_de_lansare
    program_ecrane_de_lansare.run_module('흐름시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('흐름시험')
    mapare_VALUE = {'out': 'KR_date', 'main': 'Pornește', 'ROOT': 'Project_rădăcină', 'p': 'date_poziție', 'text': 'SMS', 'report': 'validare_raport'}
    for Anteriorul_element, curent_element in mapare_VALUE.items():
        if hasattr(구현, curent_element): globals()[Anteriorul_element] = getattr(구현, curent_element)
