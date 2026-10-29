#!/usr/bin/env python3
"""기존 yo_l 호환 kiritish_nuqta. real_ma_lumotlar 구현: ../Vositalar/nashr_Terminal_shrift.py"""
import importlib as TAKE_VALUE
import sys as operatsion_tizim_VALUE
from pathlib import Path as yo_l
operatsion_tizim_VALUE.path.insert(0, str(yo_l(__file__).resolve().parents[1] / 'Vositalar'))
if __name__ == '__main__':
    import runpy as ilova_ilovalar_paneli
    ilova_ilovalar_paneli.run_module('nashr_Terminal_shrift', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('nashr_Terminal_shrift')
    대응 = {'data': 'ma_lumotlar', 'img': 'chizish_VALUE', 'bits': 'fonda_intellektual_uzatish_xizmati_Ro_yxat', 'x': 'x_koordinata', 'draw': '화면그리기', 'licences': '이용허락목록', 'paths': 'yo_l_Ro_yxat', 'y': 'Y_tugmasi_koordinat', 'main': 'Bajarish', 'src': '원본주소', 'fonts': 'shrift_Ro_yxat', 'ROOT': 'Project_ildiz', 'p': 'ma_lumotlar_holat', 'cp': 'belgi_kodlash', 'target': 'nishon'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
