#!/usr/bin/env python3
"""기존 aqqut 호환 Iliniku_puinti. taannallarik_titiqqat 구현: ../도구/올리기.py"""
import importlib as 가져오기
import sys as qarasaujakkut_aulattijjut_atuutilik
from pathlib import Path as aqqut
qarasaujakkut_aulattijjut_atuutilik.path.insert(0, str(aqqut(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('올리기', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('올리기')
    대응 = {'data': 'titiqqat', 'i': '순번', 'name': 'atiq', 'c': 'immikkuuqtumut_nalunaikkut', 'p': '자료위치', 'args': 'aturniqarnirainiq_array'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
