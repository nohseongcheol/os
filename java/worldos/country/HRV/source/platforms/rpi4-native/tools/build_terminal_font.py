#!/usr/bin/env python3
"""기존 PUTANJA 호환 unos_p. stvaran_podaci 구현: ../Alati/međuverzija_Terminal_font.py"""
import importlib as TAKE_VALUE
import sys as operacijski_sustav_VALUE
from pathlib import Path as PUTANJA
operacijski_sustav_VALUE.path.insert(0, str(PUTANJA(__file__).resolve().parents[1] / 'Alati'))
if __name__ == '__main__':
    import runpy as program_pokretač
    program_pokretač.run_module('međuverzija_Terminal_font', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('međuverzija_Terminal_font')
    mapiranje_VALUE = {'data': 'podaci', 'img': 'crtež_VALUE', 'bits': 'Pozadinski_pametni_servis_za_transfer_Popis', 'x': 'koordinata_x', 'draw': '화면그리기', 'licences': '이용허락목록', 'paths': 'put_Popis', 'y': '세로좌표', 'main': 'Pokreni', 'src': '원본주소', 'fonts': 'font_Popis', 'ROOT': 'akcija_korijen', 'p': 'podaci_položaj', 'cp': 'kodiranje_znakova', 'target': 'cilj'}
    for 이전, redovno_artikl in mapiranje_VALUE.items():
        if hasattr(구현, redovno_artikl): globals()[이전] = getattr(구현, redovno_artikl)
