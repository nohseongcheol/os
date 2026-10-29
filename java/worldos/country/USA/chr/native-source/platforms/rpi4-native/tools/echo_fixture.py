#!/usr/bin/env python3
"""기존 ᎠᏍᏓᏩᏛᏍᏗ 호환 Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᎤᏓᏓᏟ. ᎤᏙᎯᏳ_ᎾᏍᎩ_ᎨᏒ_ᎦᏟᏌᏅᎯ 구현: ../도구/되돌림시험서버.py"""
import importlib as 가져오기
import sys as ᎢᏯᏛᏁᏗ_ᏄᏍᏗᏓᏅᎢ_ᏧᎬᏩᎶᏗᏯ
from pathlib import Path as ᎠᏍᏓᏩᏛᏍᏗ
ᎢᏯᏛᏁᏗ_ᏄᏍᏗᏓᏅᎢ_ᏧᎬᏩᎶᏗᏯ.path.insert(0, str(ᎠᏍᏓᏩᏛᏍᏗ(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('되돌림시험서버', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('되돌림시험서버')
    대응 = {'data': 'ᎦᏟᏌᏅᎯ', 'e': '보조항목', 'connection': 'ᎫᏓᎸᎢ_e05f319b', 'f': 'ᎠᏍᏆᏂᎪᏙᏗ_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ', 'peer': 'ᏱᎦᏲᎩᎾᏛᏂ_ᏧᎬᏩᎶᏗᏯ', 'self': '자신', 'udp': '전문제어', 't': '터미널항목', 'tcp': 'ᎫᏓᎸᎢ_ᎠᎯᎸᏍᏗ', 'EchoFixture': '되돌림시험서버', 'args': 'ᏗᏓᎦᏘᎸᏍᏗ_array', 'chunk': '조각'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
