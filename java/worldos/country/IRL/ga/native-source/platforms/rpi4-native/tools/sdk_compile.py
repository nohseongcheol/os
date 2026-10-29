#!/usr/bin/env python3
"""기존 CONAIR 호환 iontráil_pointe. iarbhír_sonraí 구현: ../Uirlisí/SDK_tóg.py"""
import importlib as TAKE_VALUE
import sys as córas_oibriúcháin_VALUE
from pathlib import Path as CONAIR
córas_oibriúcháin_VALUE.path.insert(0, str(CONAIR(__file__).resolve().parents[1] / 'Uirlisí'))
if __name__ == '__main__':
    import runpy as clár_tarraiceán_feidhmchlár
    clár_tarraiceán_feidhmchlár.run_module('SDK_tóg', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('SDK_tóg')
    대응 = {'compiler': '번역기', 'obj': 'comhad_sprice', 'sdk': '개발꾸러미', 'output': '출력결과', 'main': 'Rith_2', 'elf': '실행파일', 'is_c': '시언어여부', 'parser': '인수해석기', 'language': 'Teanga', 'work': '작업경로', 'args': 'argóint_ARRAY'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
