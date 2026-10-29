#!/usr/bin/env python3
"""기존 wopu_a_ttaaleemüin 호환 ekeroliaa_o_uchikanain. 실제 구현: ../도구/되돌림시험서버.py"""
import importlib as 가져오기
import sys as a_yatawajiraaya_a_laülaasü_ajutuu
from pathlib import Path as wopu_a_ttaaleemüin
a_yatawajiraaya_a_laülaasü_ajutuu.path.insert(0, str(wopu_a_ttaaleemüin(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('되돌림시험서버', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('되돌림시험서버')
    대응 = {'data': 'atijaaya', 'e': '보조항목', 'connection': 'epe_ipajia_e05f319b', 'f': 'anaajaalaa_ekeroliaa', 'peer': 'wanaawasü_ajutuu', 'self': '자신', 'udp': '전문제어', 't': '터미널항목', 'tcp': 'epe_ipajia_aa_inmajia', 'EchoFixture': '되돌림시험서버', 'args': 'ajutuu_matüriisü', 'chunk': '조각'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
