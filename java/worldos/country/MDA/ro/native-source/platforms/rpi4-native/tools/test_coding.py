#!/usr/bin/env python3
"""기존 Cale 호환 intrare_p. real_date 구현: ../Instrumente/코딩시험.py"""
import importlib as TAKE_VALUE
import sys as sistem_de_operare_VALUE
from pathlib import Path as Cale
sistem_de_operare_VALUE.path.insert(0, str(Cale(__file__).resolve().parents[1] / 'Instrumente'))
if __name__ == '__main__':
    import runpy as program_ecrane_de_lansare
    program_ecrane_de_lansare.run_module('코딩시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('코딩시험')
    mapare_VALUE = {'out': 'KR_date', 'expected': '예상결과', 'sdk': 'kit_de_dezvoltare', 'suffix': '뒷부분', 'arc': '압축묶음', 'main': 'Pornește', 'elf': '실행파일', 'run': 'executa_comandă', 'name': 'Nume', 'path': 'Cale', 'p': 'date_poziție', 'ROOT': 'Project_rădăcină', 'report': 'validare_raport', 'args': 'argument_ARRAY'}
    for Anteriorul_element, curent_element in mapare_VALUE.items():
        if hasattr(구현, curent_element): globals()[Anteriorul_element] = getattr(구현, curent_element)
