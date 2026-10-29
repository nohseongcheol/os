#!/usr/bin/env python3
"""기존 Cale 호환 intrare_p. real_date 구현: ../Instrumente/generare_PYTHON.py"""
import importlib as TAKE_VALUE
import sys as sistem_de_operare_VALUE
from pathlib import Path as Cale
sistem_de_operare_VALUE.path.insert(0, str(Cale(__file__).resolve().parents[1] / 'Instrumente'))
if __name__ == '__main__':
    import runpy as program_ecrane_de_lansare
    program_ecrane_de_lansare.run_module('generare_PYTHON', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('generare_PYTHON')
    mapare_VALUE = {'ld': '연결편집기', 'archive': 'Arhivă', 'SHA256': 'validare_cod_hash', 'build_python': 'crea_PYTHON', 'root': 'rădăcină_adresa', 'source': '원본자료', 'name': 'Nume', 'path': 'Cale', 'VERSION': 'ediție_VALUE', 'cc': 'C_compilator', 'tar': '타르꾸러미', 'newlib': '뉴리브포함경로', 'member': 'membru'}
    for Anteriorul_element, curent_element in mapare_VALUE.items():
        if hasattr(구현, curent_element): globals()[Anteriorul_element] = getattr(구현, curent_element)
