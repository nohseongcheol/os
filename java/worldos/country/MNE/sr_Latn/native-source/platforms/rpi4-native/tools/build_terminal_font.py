#!/usr/bin/env python3
"""기존 putanja 호환 stavka_p. stvarni_podaci 구현: ../Alatke/verzija_Terminal_font.py"""
import importlib as TAKE_VALUE
import sys as operativni_sistem_VALUE
from pathlib import Path as putanja
operativni_sistem_VALUE.path.insert(0, str(putanja(__file__).resolve().parents[1] / 'Alatke'))
if __name__ == '__main__':
    import runpy as program_pokretač
    program_pokretač.run_module('verzija_Terminal_font', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('verzija_Terminal_font')
    mapiranje_VALUE = {'data': 'podaci', 'img': 'crtež_VALUE', 'bits': 'Usluga_inteligentnog_prenosa_u_pozadini_Lista', 'x': 'x_koordinata', 'draw': '화면그리기', 'licences': '이용허락목록', 'paths': 'putanja_Lista', 'y': '세로좌표', 'main': 'koristiti', 'src': '원본주소', 'fonts': 'font_Lista', 'ROOT': 'radnja_koren', 'p': 'podaci_pozicija', 'cp': 'kodiranje_znakova', 'target': 'cilj'}
    for 이전, aktuelno_stavka in mapiranje_VALUE.items():
        if hasattr(구현, aktuelno_stavka): globals()[이전] = getattr(구현, aktuelno_stavka)
