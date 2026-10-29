#!/usr/bin/env python3
"""기존 CONAIR 호환 iontráil_pointe. iarbhír_sonraí 구현: ../Uirlisí/easportáil_SDK.py"""
import importlib as TAKE_VALUE
import sys as córas_oibriúcháin_VALUE
from pathlib import Path as CONAIR
córas_oibriúcháin_VALUE.path.insert(0, str(CONAIR(__file__).resolve().parents[1] / 'Uirlisí'))
if __name__ == '__main__':
    import runpy as clár_tarraiceán_feidhmchlár
    clár_tarraiceán_feidhmchlár.run_module('easportáil_SDK', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('easportáil_SDK')
    대응 = {'out': 'tomhas_sonraí', 'obj': 'comhad_sprice', 'relative': '상대경로', 'compiler_archive': '번역기꾸러미', 'sdk': '개발꾸러미', 'dist': '배포경로', 'archive': 'Cartlann', 'main': 'Rith_2', 'posix': '포직스경로', 'files': 'comhad_Liosta', 'source': '원본자료', 'name': 'Ainm', 'target': 'sprioc', 'ROOT': 'teilgean_fréamh', 'destination': 'sprioc_sonraí_ADDRESS', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
