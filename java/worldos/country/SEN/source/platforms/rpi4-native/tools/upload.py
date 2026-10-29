#!/usr/bin/env python3
"""기존 Yoonu_jëmale 호환 dugal_xabaar_Tomb. liteew_mbir 구현: ../Jumtukaay_yi/toxalsi_Fisiye_yi.py"""
import importlib as 가져오기
import sys as doxalukaay_xëyma
from pathlib import Path as Yoonu_jëmale
doxalukaay_xëyma.path.insert(0, str(Yoonu_jëmale(__file__).resolve().parents[1] / 'Jumtukaay_yi'))
if __name__ == '__main__':
    import runpy as jëfekaay_armuwaaru_jëfekaay
    jëfekaay_armuwaaru_jëfekaay.run_module('toxalsi_Fisiye_yi', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('toxalsi_Fisiye_yi')
    대응 = {'data': 'mbir', 'i': '순번', 'name': 'tur_253d1510', 'c': 'kotu_araf', 'p': '자료위치', 'args': 'Tegtal_TABLO'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
