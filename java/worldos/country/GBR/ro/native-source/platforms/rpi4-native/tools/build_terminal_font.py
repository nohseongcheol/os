#!/usr/bin/env python3
"""기존 Cale 호환 intrare_p. real_date 구현: ../Instrumente/generare_Terminal_font.py"""
import importlib as TAKE_VALUE
import sys as sistem_de_operare_VALUE
from pathlib import Path as Cale
sistem_de_operare_VALUE.path.insert(0, str(Cale(__file__).resolve().parents[1] / 'Instrumente'))
if __name__ == '__main__':
    import runpy as program_ecrane_de_lansare
    program_ecrane_de_lansare.run_module('generare_Terminal_font', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('generare_Terminal_font')
    mapare_VALUE = {'data': 'date', 'img': 'desen_VALUE', 'bits': 'Serviciu_de_transfer_inteligent_în_fundal_Listă', 'x': 'coordonata_X', 'draw': '화면그리기', 'licences': '이용허락목록', 'paths': 'cale_Listă', 'y': '세로좌표', 'main': 'Pornește', 'src': '원본주소', 'fonts': 'font_Listă', 'ROOT': 'Project_rădăcină', 'p': 'date_poziție', 'cp': 'codificare_caractere', 'target': 'țintă'}
    for Anteriorul_element, curent_element in mapare_VALUE.items():
        if hasattr(구현, curent_element): globals()[Anteriorul_element] = getattr(구현, curent_element)
