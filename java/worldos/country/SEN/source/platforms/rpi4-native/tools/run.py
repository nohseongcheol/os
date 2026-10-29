#!/usr/bin/env python3
"""기존 Yoonu_jëmale 호환 dugal_xabaar_Tomb. liteew_mbir 구현: ../Jumtukaay_yi/def_ndigel.py"""
import importlib as 가져오기
import sys as doxalukaay_xëyma
from pathlib import Path as Yoonu_jëmale
doxalukaay_xëyma.path.insert(0, str(Yoonu_jëmale(__file__).resolve().parents[1] / 'Jumtukaay_yi'))
if __name__ == '__main__':
    import runpy as jëfekaay_armuwaaru_jëfekaay
    jëfekaay_armuwaaru_jëfekaay.run_module('def_ndigel', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('def_ndigel')
    대응 = {'supported': '지원목록', 'parser': '인수해석기', 'qemu': '모의기계', 'run_desktop': 'daw_Biro', 'main': 'daw', 'host': 'dalal', 'status': 'nekkin_xëyma', 'NetworkBridge': 'mbaal_poŋ', 'ROOT': '기준', 'bridge': 'poŋ', 'loader': '적재기', 'base': 'Njiitlay_xëyma', 'options': 'tànneef', 'binary': 'Seexalin_ci_kaw_0_et1', 'args': 'Tegtal_TABLO', 'command': 'ndigel'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
