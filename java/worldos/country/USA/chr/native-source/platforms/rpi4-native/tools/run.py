#!/usr/bin/env python3
"""기존 ᎠᏍᏓᏩᏛᏍᏗ 호환 Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᎤᏓᏓᏟ. ᎤᏙᎯᏳ_ᎾᏍᎩ_ᎨᏒ_ᎦᏟᏌᏅᎯ 구현: ../도구/ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ.py"""
import importlib as 가져오기
import sys as ᎢᏯᏛᏁᏗ_ᏄᏍᏗᏓᏅᎢ_ᏧᎬᏩᎶᏗᏯ
from pathlib import Path as ᎠᏍᏓᏩᏛᏍᏗ
ᎢᏯᏛᏁᏗ_ᏄᏍᏗᏓᏅᎢ_ᏧᎬᏩᎶᏗᏯ.path.insert(0, str(ᎠᏍᏓᏩᏛᏍᏗ(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ')
    대응 = {'supported': '지원목록', 'parser': '인수해석기', 'qemu': '모의기계', 'run_desktop': 'ᎠᎢᏎᏍᏗ_ᎦᏍᎩᎶᎩ_ᎦᏚ', 'main': 'ᎠᎢᏎᏍᏗ', 'host': 'ᎠᏁᏢᏍᎩ', 'status': 'ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ', 'NetworkBridge': '통신다리', 'ROOT': '기준', 'bridge': '연결다리', 'loader': '적재기', 'base': 'ᎠᏍᏆᏚᎸ_ᎦᏯᎸᏗ_ᏧᎬᏩᎶᏗᏯ', 'options': 'ᎠᏑᏰᏍᏗᎢ', 'binary': 'binary', 'args': 'ᏗᏓᎦᏘᎸᏍᏗ_array', 'command': 'ᎤᏁᏤᎸᎩ'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
