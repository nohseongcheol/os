#!/usr/bin/env python3
"""기존 tsela 호환 tsenyo_ntlha. tota_tshedimosetso 구현: ../Thuluse/diragatsa_Taelo.py"""
import importlib as 가져오기
import sys as Tsamaisotiriso_Boleng
from pathlib import Path as tsela
Tsamaisotiriso_Boleng.path.insert(0, str(tsela(__file__).resolve().parents[1] / 'Thuluse'))
if __name__ == '__main__':
    import runpy as Tiriso_llae_ya_sediriso
    Tiriso_llae_ya_sediriso.run_module('diragatsa_Taelo', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('diragatsa_Taelo')
    대응 = {'supported': '지원목록', 'parser': '인수해석기', 'qemu': '모의기계', 'run_desktop': 'dirisa_desekethopo', 'main': 'dirisa', 'host': 'pinagare', 'status': 'kemo_Boleng', 'NetworkBridge': 'Neteweke_leborogo', 'ROOT': '기준', 'bridge': 'leborogo', 'loader': '적재기', 'base': 'Lemorago_Boleng', 'options': 'Diitlhophelwa', 'binary': 'baenari', 'args': 'Thulaganyo_setlhopha', 'command': 'Taelo'}
    for 이전, ga_jaana_selwana in 대응.items():
        if hasattr(구현, ga_jaana_selwana): globals()[이전] = getattr(구현, ga_jaana_selwana)
