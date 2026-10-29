#!/usr/bin/env python3
"""기존 Cale 호환 intrare_p. real_date 구현: ../Instrumente/generare_C_compilator.py"""
import importlib as TAKE_VALUE
import sys as sistem_de_operare_VALUE
from pathlib import Path as Cale
sistem_de_operare_VALUE.path.insert(0, str(Cale(__file__).resolve().parents[1] / 'Instrumente'))
if __name__ == '__main__':
    import runpy as program_ecrane_de_lansare
    program_ecrane_de_lansare.run_module('generare_C_compilator', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('generare_C_compilator')
    mapare_VALUE = {'out': 'KR_date', 'builtins': '내장연산', 'header': 'Antet_VALUE', 'sdk': 'kit_de_dezvoltare', 'build_ccompiler': 'crea_C_compilator', 'i': '순번', 'elf': '실행파일', 'run': 'executa_comandă', 'flags': 'configurație_Serviciu_de_transfer_inteligent_în_fundal', 'path': 'Cale', 'p': 'date_poziție', 'cc': 'C_compilator', 'obj': 'fișier_destinație', 'flag': 'Setări_VALUE', 'ld': '연결편집기', 'objects': 'destinație_Fișiere', 'repo': 'depozit_cale', 'v': '임시값', 'upstream': 'în_amonte', 'root': 'rădăcină_adresa', 'assets': '탑재자료', 'source': '원본자료', 'name': 'Nume', 'includes': '포함인수'}
    for Anteriorul_element, curent_element in mapare_VALUE.items():
        if hasattr(구현, curent_element): globals()[Anteriorul_element] = getattr(구현, curent_element)
