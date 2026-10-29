#!/usr/bin/env python3
"""기존 aqqut 호환 Iliniku_puinti. taannallarik_titiqqat 구현: ../도구/코딩시험.py"""
import importlib as 가져오기
import sys as qarasaujakkut_aulattijjut_atuutilik
from pathlib import Path as aqqut
qarasaujakkut_aulattijjut_atuutilik.path.insert(0, str(aqqut(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('코딩시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('코딩시험')
    대응 = {'out': '결과자료', 'expected': '예상결과', 'sdk': '개발꾸러미', 'suffix': '뒷부분', 'arc': '압축묶음', 'main': '시작', 'elf': '실행파일', 'run': '실행', 'name': 'atiq', 'path': 'aqqut', 'p': '자료위치', 'ROOT': '기준', 'report': 'naammannirainiq_unikkaaq', 'args': 'aturniqarnirainiq_array'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
