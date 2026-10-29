#!/usr/bin/env python3
"""기존 LLWYBR 호환 cofnod_p. go_iawn_data 구현: ../Offer/llunio_Terfynell_ffont.py"""
import importlib as TAKE_VALUE
import sys as system_weithredu_VALUE
from pathlib import Path as LLWYBR
system_weithredu_VALUE.path.insert(0, str(LLWYBR(__file__).resolve().parents[1] / 'Offer'))
if __name__ == '__main__':
    import runpy as Rhaglen_lansiwr
    Rhaglen_lansiwr.run_module('llunio_Terfynell_ffont', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('llunio_Terfynell_ffont')
    대응 = {'data': 'data', 'img': 'lluniad_VALUE', 'bits': '비트들', 'x': 'cyfesuryn_x', 'draw': '화면그리기', 'licences': '이용허락목록', 'paths': 'llwybr_Rhestr', 'y': 'Y_cyfesuryn', 'main': 'Gweithredu_2', 'src': '원본주소', 'fonts': 'ffont_Rhestr', 'ROOT': 'prosiect_gwraidd', 'p': 'data_safle', 'cp': 'nod_amgodio', 'target': 'targed'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
