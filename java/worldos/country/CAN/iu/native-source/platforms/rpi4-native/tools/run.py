#!/usr/bin/env python3
"""기존 aqqut 호환 Iliniku_puinti. taannallarik_titiqqat 구현: ../도구/실행.py"""
import importlib as 가져오기
import sys as qarasaujakkut_aulattijjut_atuutilik
from pathlib import Path as aqqut
qarasaujakkut_aulattijjut_atuutilik.path.insert(0, str(aqqut(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('실행', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('실행')
    대응 = {'supported': '지원목록', 'parser': '인수해석기', 'qemu': '모의기계', 'run_desktop': '바탕화면실행', 'main': '시작', 'host': 'tuttarvik', 'status': 'qanuilinganiq_atuutilik', 'NetworkBridge': '통신다리', 'ROOT': '기준', 'bridge': '연결다리', 'loader': '적재기', 'base': 'ungataa_atuutilik', 'options': 'Qanuqtuurutit', 'binary': 'binary', 'args': 'aturniqarnirainiq_array', 'command': 'piqujijjut'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
