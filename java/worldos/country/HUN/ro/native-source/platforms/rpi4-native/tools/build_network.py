#!/usr/bin/env python3
"""기존 Cale 호환 intrare_p. real_date 구현: ../Instrumente/generare_rețea.py"""
import importlib as TAKE_VALUE
import sys as sistem_de_operare_VALUE
from pathlib import Path as Cale
sistem_de_operare_VALUE.path.insert(0, str(Cale(__file__).resolve().parents[1] / 'Instrumente'))
if __name__ == '__main__':
    import runpy as program_ecrane_de_lansare
    program_ecrane_de_lansare.run_module('generare_rețea', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('generare_rețea')
    mapare_VALUE = {'obj': 'fișier_destinație', 'objects': 'destinație_Fișiere', 'library': 'bibliotecă', 'output': '출력결과', 'port': 'număr_port', 'root': 'rădăcină_adresa', 'files': 'Fișier_Listă', 'source': '원본자료', 'run': 'executa_comandă', 'flags': 'configurație_Serviciu_de_transfer_inteligent_în_fundal', 'path': 'Cale', 'build_network': 'crea_rețea_48d29d6d', 'cc': 'C_compilator', 'ar': 'Arhivă_instrument'}
    for Anteriorul_element, curent_element in mapare_VALUE.items():
        if hasattr(구현, curent_element): globals()[Anteriorul_element] = getattr(구현, curent_element)
