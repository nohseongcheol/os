#!/usr/bin/env python3
"""기존 njia 호환 ingizo_pointi. halisi_data 구현: ../Zana/pakia_Faili.py"""
import importlib as 가져오기
import sys as mfumo_endeshi_thamani
from pathlib import Path as njia
mfumo_endeshi_thamani.path.insert(0, str(njia(__file__).resolve().parents[1] / 'Zana'))
if __name__ == '__main__':
    import runpy as programu_droo_ya_programu
    programu_droo_ya_programu.run_module('pakia_Faili', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('pakia_Faili')
    대응 = {'data': 'data', 'i': '순번', 'name': 'Jina', 'c': 'msimbo_wa_kibambo', 'p': '자료위치', 'args': 'hoja_ARRAY'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
