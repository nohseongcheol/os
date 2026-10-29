#!/usr/bin/env python3
"""기존 Ýol 호환 girizmeklik_utuk. hakyky_maglumat 구현: ../Gurallar/ýerine_ýetir_buýruk.py"""
import importlib as 가져오기
import sys as operasiýa_ulgamy_baha
from pathlib import Path as Ýol
operasiýa_ulgamy_baha.path.insert(0, str(Ýol(__file__).resolve().parents[1] / 'Gurallar'))
if __name__ == '__main__':
    import runpy as programma_programma_paneli
    programma_programma_paneli.run_module('ýerine_ýetir_buýruk', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ýerine_ýetir_buýruk')
    대응 = {'supported': '지원목록', 'parser': '인수해석기', 'qemu': '모의기계', 'run_desktop': 'işe_goýber_iş_stoly', 'main': 'Bitir', 'host': 'esasy', 'status': 'ýagdaý_baha', 'NetworkBridge': '통신다리', 'ROOT': '기준', 'bridge': '연결다리', 'loader': '적재기', 'base': 'Fon_baha', 'options': 'Opsiýalar', 'binary': 'ikilik', 'args': 'argument_ARRAY', 'command': 'buýruk'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
