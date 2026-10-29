#!/usr/bin/env python3
"""기존 Putanja 호환 unos_p. stvaran_podaci 구현: ../Alati/verzija_Terminal_font.py"""
import importlib as TAKE_VALUE
import sys as operativni_sistem_VALUE
from pathlib import Path as Putanja
operativni_sistem_VALUE.path.insert(0, str(Putanja(__file__).resolve().parents[1] / 'Alati'))
if __name__ == '__main__':
    import runpy as program_pokretač
    program_pokretač.run_module('verzija_Terminal_font', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('verzija_Terminal_font')
    대응 = {'data': 'podaci', 'img': 'ucrtavanje_VALUE', 'bits': '비트들', 'x': 'koordinata_x', 'draw': '화면그리기', 'licences': '이용허락목록', 'paths': 'put_spisak', 'y': 'Y_koordinata', 'main': 'Pokreni', 'src': '원본주소', 'fonts': 'font_spisak', 'ROOT': 'projicirati_koijen', 'p': 'podaci_položaj', 'cp': 'znak_kodiranje', 'target': 'cilj'}
    for 이전, trenutno_stavka in 대응.items():
        if hasattr(구현, trenutno_stavka): globals()[이전] = getattr(구현, trenutno_stavka)
