#!/usr/bin/env python3
"""기존 njia 호환 ingizo_pointi. halisi_data 구현: ../Zana/SDK_jenga.py"""
import importlib as 가져오기
import sys as mfumo_endeshi_thamani
from pathlib import Path as njia
mfumo_endeshi_thamani.path.insert(0, str(njia(__file__).resolve().parents[1] / 'Zana'))
if __name__ == '__main__':
    import runpy as programu_droo_ya_programu
    programu_droo_ya_programu.run_module('SDK_jenga', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('SDK_jenga')
    대응 = {'compiler': '번역기', 'obj': 'faili_fikio', 'sdk': '개발꾸러미', 'output': '출력결과', 'main': 'endesha', 'elf': '실행파일', 'is_c': '시언어여부', 'parser': 'kichanganuzi', 'language': 'Lugha', 'work': '작업경로', 'args': 'hoja_ARRAY'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
