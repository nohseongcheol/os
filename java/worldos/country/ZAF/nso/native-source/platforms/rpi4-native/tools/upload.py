#!/usr/bin/env python3
"""기존 Tsejana 호환 go_tsenya_tshedimošo_ntlha. kgonthe_data 구현: ../Ditholosi/apolouto_Difaele.py"""
import importlib as 가져오기
import sys as tshepedišotirišo_boleng
from pathlib import Path as Tsejana
tshepedišotirišo_boleng.path.insert(0, str(Tsejana(__file__).resolve().parents[1] / 'Ditholosi'))
if __name__ == '__main__':
    import runpy as tirišo_sethala_tirišo
    tirišo_sethala_tirišo.run_module('apolouto_Difaele', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('apolouto_Difaele')
    대응 = {'data': 'data', 'i': '순번', 'name': 'Leina', 'c': 'khouto_ya_tlhaka', 'p': '자료위치', 'args': 'akumente_arei'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
