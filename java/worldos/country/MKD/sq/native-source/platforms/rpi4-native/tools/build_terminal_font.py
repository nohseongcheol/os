#!/usr/bin/env python3
"""기존 POZICIONI 호환 futje_p. aktual_të_dhëna 구현: ../Mjete/ndërtoj_Terminali_font.py"""
import importlib as TAKE_VALUE
import sys as sistem_operativ_VALUE
from pathlib import Path as POZICIONI
sistem_operativ_VALUE.path.insert(0, str(POZICIONI(__file__).resolve().parents[1] / 'Mjete'))
if __name__ == '__main__':
    import runpy as program_hapës
    program_hapës.run_module('ndërtoj_Terminali_font', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('ndërtoj_Terminali_font')
    대응 = {'data': 'të_dhëna', 'img': 'vizatim_VALUE', 'bits': 'Shërbimi_i_transferimit_inteligjent_në_sfond_Listë', 'x': 'koordinata_x', 'draw': '화면그리기', 'licences': '이용허락목록', 'paths': 'shteg_Listë', 'y': 'Y_koordinatë', 'main': 'Ekzekuto', 'src': '원본주소', 'fonts': 'font_Listë', 'ROOT': 'Project_rrënjë', 'p': 'të_dhëna_pozicioni', 'cp': 'karakter_enkodim', 'target': 'objektiv'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
