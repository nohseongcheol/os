#!/usr/bin/env python3
"""기존 Slighe 호환 cur_a_steach_puing. dearbh_dàta 구현: ../innealan/개발꾸러미번역.py"""
import importlib as TAKE_VALUE
import sys as siostam_obrachaidh_VALUE
from pathlib import Path as Slighe
siostam_obrachaidh_VALUE.path.insert(0, str(Slighe(__file__).resolve().parents[1] / 'innealan'))
if __name__ == '__main__':
    import runpy as ap_drathair_nan_aplacaid
    ap_drathair_nan_aplacaid.run_module('개발꾸러미번역', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('개발꾸러미번역')
    대응 = {'compiler': '번역기', 'obj': 'faidhle_uidhe', 'sdk': '개발꾸러미', 'output': '출력결과', 'main': 'ruith', 'elf': '실행파일', 'is_c': '시언어여부', 'parser': '인수해석기', 'language': 'cànan', 'work': '작업경로', 'args': 'argamaid_ARRAY'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
