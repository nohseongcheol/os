#!/usr/bin/env python3
"""기존 CONAIR 호환 iontráil_pointe. iarbhír_sonraí 구현: ../Uirlisí/Rith_ordú.py"""
import importlib as TAKE_VALUE
import sys as córas_oibriúcháin_VALUE
from pathlib import Path as CONAIR
córas_oibriúcháin_VALUE.path.insert(0, str(CONAIR(__file__).resolve().parents[1] / 'Uirlisí'))
if __name__ == '__main__':
    import runpy as clár_tarraiceán_feidhmchlár
    clár_tarraiceán_feidhmchlár.run_module('Rith_ordú', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('Rith_ordú')
    대응 = {'supported': '지원목록', 'parser': '인수해석기', 'qemu': '모의기계', 'run_desktop': 'rith_deasc', 'main': 'Rith_2', 'host': 'óstach', 'status': 'staid_VALUE', 'NetworkBridge': 'Líonra_traschóiritheoir', 'ROOT': 'teilgean_fréamh', 'bridge': 'traschóiritheoir', 'loader': '적재기', 'base': 'Cúlra_VALUE', 'options': 'Roghanna', 'binary': 'dénártha', 'args': 'argóint_ARRAY', 'command': 'Ordú'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
