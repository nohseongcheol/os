#!/usr/bin/env python3
"""기존 njia 호환 ingizo_pointi. halisi_data 구현: ../Zana/tekeleza_amri.py"""
import importlib as 가져오기
import sys as mfumo_endeshi_thamani
from pathlib import Path as njia
mfumo_endeshi_thamani.path.insert(0, str(njia(__file__).resolve().parents[1] / 'Zana'))
if __name__ == '__main__':
    import runpy as programu_droo_ya_programu
    programu_droo_ya_programu.run_module('tekeleza_amri', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('tekeleza_amri')
    대응 = {'supported': '지원목록', 'parser': 'kichanganuzi', 'qemu': '모의기계', 'run_desktop': 'endesha_Eneo_kazi', 'main': 'endesha', 'host': 'mwenyeji', 'status': 'hali_thamani', 'NetworkBridge': 'Mtandao_daraja', 'ROOT': '기준', 'bridge': 'daraja', 'loader': '적재기', 'base': 'nyuma_thamani', 'options': 'chaguo', 'binary': 'jozi', 'args': 'hoja_ARRAY', 'command': 'amri'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
