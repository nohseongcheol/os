#!/usr/bin/env python3
"""기존 Cale 호환 intrare_p. real_date 구현: ../Instrumente/SDK_compilare.py"""
import importlib as TAKE_VALUE
import sys as sistem_de_operare_VALUE
from pathlib import Path as Cale
sistem_de_operare_VALUE.path.insert(0, str(Cale(__file__).resolve().parents[1] / 'Instrumente'))
if __name__ == '__main__':
    import runpy as program_ecrane_de_lansare
    program_ecrane_de_lansare.run_module('SDK_compilare', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('SDK_compilare')
    mapare_VALUE = {'compiler': 'compilator_instrument', 'obj': 'fișier_destinație', 'sdk': 'kit_de_dezvoltare', 'output': '출력결과', 'main': 'Pornește', 'elf': '실행파일', 'is_c': 'sisteme_de_informații_C_Limbi_străine', 'parser': 'parser', 'language': 'Limbi_străine', 'work': '작업경로', 'args': 'argument_ARRAY'}
    for Anteriorul_element, curent_element in mapare_VALUE.items():
        if hasattr(구현, curent_element): globals()[Anteriorul_element] = getattr(구현, curent_element)
