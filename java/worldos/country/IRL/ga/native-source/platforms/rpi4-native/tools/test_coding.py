#!/usr/bin/env python3
"""기존 CONAIR 호환 iontráil_pointe. iarbhír_sonraí 구현: ../Uirlisí/코딩시험.py"""
import importlib as TAKE_VALUE
import sys as córas_oibriúcháin_VALUE
from pathlib import Path as CONAIR
córas_oibriúcháin_VALUE.path.insert(0, str(CONAIR(__file__).resolve().parents[1] / 'Uirlisí'))
if __name__ == '__main__':
    import runpy as clár_tarraiceán_feidhmchlár
    clár_tarraiceán_feidhmchlár.run_module('코딩시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('코딩시험')
    대응 = {'out': 'tomhas_sonraí', 'expected': '예상결과', 'sdk': '개발꾸러미', 'suffix': '뒷부분', 'arc': '압축묶음', 'main': 'Rith_2', 'elf': '실행파일', 'run': 'Rith_ordú', 'name': 'Ainm', 'path': 'CONAIR', 'p': 'sonraí_suíomh', 'ROOT': 'teilgean_fréamh', 'report': 'bailíochtú_tuairisc', 'args': 'argóint_ARRAY'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
