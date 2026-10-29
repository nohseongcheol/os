#!/usr/bin/env python3
"""기존 tsela 호환 tsenyo_ntlha. tota_tshedimosetso 구현: ../Thuluse/laisa_Difaele.py"""
import importlib as 가져오기
import sys as Tsamaisotiriso_Boleng
from pathlib import Path as tsela
Tsamaisotiriso_Boleng.path.insert(0, str(tsela(__file__).resolve().parents[1] / 'Thuluse'))
if __name__ == '__main__':
    import runpy as Tiriso_llae_ya_sediriso
    Tiriso_llae_ya_sediriso.run_module('laisa_Difaele', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('laisa_Difaele')
    대응 = {'data': 'tshedimosetso', 'i': '순번', 'name': 'leina', 'c': 'khoutuletshwao', 'p': '자료위치', 'args': 'Thulaganyo_setlhopha'}
    for 이전, ga_jaana_selwana in 대응.items():
        if hasattr(구현, ga_jaana_selwana): globals()[이전] = getattr(구현, ga_jaana_selwana)
