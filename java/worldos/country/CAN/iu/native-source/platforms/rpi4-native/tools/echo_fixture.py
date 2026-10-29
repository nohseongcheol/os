#!/usr/bin/env python3
"""기존 aqqut 호환 Iliniku_puinti. taannallarik_titiqqat 구현: ../도구/되돌림시험서버.py"""
import importlib as 가져오기
import sys as qarasaujakkut_aulattijjut_atuutilik
from pathlib import Path as aqqut
qarasaujakkut_aulattijjut_atuutilik.path.insert(0, str(aqqut(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('되돌림시험서버', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('되돌림시험서버')
    대응 = {'data': 'titiqqat', 'e': '보조항목', 'connection': 'kasuqsimaniq_e05f319b', 'f': 'ini_Iliniku', 'peer': 'ilagijaujuq_atuutilik', 'self': '자신', 'udp': '전문제어', 't': '터미널항목', 'tcp': 'kasuqsimaniq_aulattivik', 'EchoFixture': '되돌림시험서버', 'args': 'aturniqarnirainiq_array', 'chunk': '조각'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
