#!/usr/bin/env python3
"""기존 tsela 호환 tsenyo_ntlha. tota_tshedimosetso 구현: ../Thuluse/코딩시험.py"""
import importlib as 가져오기
import sys as Tsamaisotiriso_Boleng
from pathlib import Path as tsela
Tsamaisotiriso_Boleng.path.insert(0, str(tsela(__file__).resolve().parents[1] / 'Thuluse'))
if __name__ == '__main__':
    import runpy as Tiriso_llae_ya_sediriso
    Tiriso_llae_ya_sediriso.run_module('코딩시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('코딩시험')
    대응 = {'out': '결과자료', 'expected': '예상결과', 'sdk': '개발꾸러미', 'suffix': '뒷부분', 'arc': '압축묶음', 'main': 'dirisa', 'elf': '실행파일', 'run': 'diragatsa_Taelo', 'name': 'leina', 'path': 'tsela', 'p': '자료위치', 'ROOT': '기준', 'report': 'netefatso_pego', 'args': 'Thulaganyo_setlhopha'}
    for 이전, ga_jaana_selwana in 대응.items():
        if hasattr(구현, ga_jaana_selwana): globals()[이전] = getattr(구현, ga_jaana_selwana)
