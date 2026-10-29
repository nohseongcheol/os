#!/usr/bin/env python3
"""기존 CONAIR 호환 iontráil_pointe. iarbhír_sonraí 구현: ../Uirlisí/tóg_Teirminéal_clófhoireann.py"""
import importlib as TAKE_VALUE
import sys as córas_oibriúcháin_VALUE
from pathlib import Path as CONAIR
córas_oibriúcháin_VALUE.path.insert(0, str(CONAIR(__file__).resolve().parents[1] / 'Uirlisí'))
if __name__ == '__main__':
    import runpy as clár_tarraiceán_feidhmchlár
    clár_tarraiceán_feidhmchlár.run_module('tóg_Teirminéal_clófhoireann', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('tóg_Teirminéal_clófhoireann')
    대응 = {'data': 'sonraí', 'img': 'líníocht_VALUE', 'bits': '비트들', 'x': 'x_chomhordanáid', 'draw': '화면그리기', 'licences': '이용허락목록', 'paths': 'cosán_Liosta', 'y': '세로좌표', 'main': 'Rith_2', 'src': '원본주소', 'fonts': 'clófhoireann_Liosta', 'ROOT': 'teilgean_fréamh', 'p': 'sonraí_suíomh', 'cp': 'carachtar_ionchódú', 'target': 'sprioc'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
