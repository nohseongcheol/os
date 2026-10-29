#!/usr/bin/env python3
"""기존 Cale 호환 intrare_p. real_date 구현: ../Instrumente/exporta_SDK.py"""
import importlib as TAKE_VALUE
import sys as sistem_de_operare_VALUE
from pathlib import Path as Cale
sistem_de_operare_VALUE.path.insert(0, str(Cale(__file__).resolve().parents[1] / 'Instrumente'))
if __name__ == '__main__':
    import runpy as program_ecrane_de_lansare
    program_ecrane_de_lansare.run_module('exporta_SDK', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('exporta_SDK')
    mapare_VALUE = {'out': 'KR_date', 'obj': 'fișier_destinație', 'relative': 'cale_relativă', 'compiler_archive': 'compilator_Arhivă', 'sdk': 'kit_de_dezvoltare', 'dist': '배포경로', 'archive': 'Arhivă', 'main': 'Pornește', 'posix': '포직스경로', 'files': 'Fișier_Listă', 'source': '원본자료', 'name': 'Nume', 'target': 'țintă', 'ROOT': 'Project_rădăcină', 'destination': 'destinație_date_adresa', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for Anteriorul_element, curent_element in mapare_VALUE.items():
        if hasattr(구현, curent_element): globals()[Anteriorul_element] = getattr(구현, curent_element)
