#!/usr/bin/env python3
"""기존 CONAIR 호환 iontráil_pointe. iarbhír_sonraí 구현: ../Uirlisí/uaslódáil_Comhaid.py"""
import importlib as TAKE_VALUE
import sys as córas_oibriúcháin_VALUE
from pathlib import Path as CONAIR
córas_oibriúcháin_VALUE.path.insert(0, str(CONAIR(__file__).resolve().parents[1] / 'Uirlisí'))
if __name__ == '__main__':
    import runpy as clár_tarraiceán_feidhmchlár
    clár_tarraiceán_feidhmchlár.run_module('uaslódáil_Comhaid', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('uaslódáil_Comhaid')
    대응 = {'data': 'sonraí', 'i': '순번', 'name': 'Ainm', 'c': 'pointe_cóid', 'p': 'sonraí_suíomh', 'args': 'argóint_ARRAY'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
