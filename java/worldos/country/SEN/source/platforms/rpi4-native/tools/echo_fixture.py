#!/usr/bin/env python3
"""기존 Yoonu_jëmale 호환 dugal_xabaar_Tomb. liteew_mbir 구현: ../Jumtukaay_yi/되돌림시험서버.py"""
import importlib as 가져오기
import sys as doxalukaay_xëyma
from pathlib import Path as Yoonu_jëmale
doxalukaay_xëyma.path.insert(0, str(Yoonu_jëmale(__file__).resolve().parents[1] / 'Jumtukaay_yi'))
if __name__ == '__main__':
    import runpy as jëfekaay_armuwaaru_jëfekaay
    jëfekaay_armuwaaru_jëfekaay.run_module('되돌림시험서버', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('되돌림시험서버')
    대응 = {'data': 'mbir', 'e': '보조항목', 'connection': 'jokkalóo_e05f319b', 'f': 'bara_denc_dugal_xabaar', 'peer': 'Nàttangoo_xëyma', 'self': '자신', 'udp': '전문제어', 't': '터미널항목', 'tcp': 'jokkalóo_Saytu_doxinu_ordinateur', 'EchoFixture': '되돌림시험서버', 'args': 'Tegtal_TABLO', 'chunk': '조각'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
