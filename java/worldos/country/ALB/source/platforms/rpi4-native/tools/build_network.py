#!/usr/bin/env python3
"""기존 POZICIONI 호환 futje_p. aktual_të_dhëna 구현: ../Mjete/ndërtoj_rrjet.py"""
import importlib as TAKE_VALUE
import sys as sistem_operativ_VALUE
from pathlib import Path as POZICIONI
sistem_operativ_VALUE.path.insert(0, str(POZICIONI(__file__).resolve().parents[1] / 'Mjete'))
if __name__ == '__main__':
    import runpy as program_hapës
    program_hapës.run_module('ndërtoj_rrjet', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('ndërtoj_rrjet')
    대응 = {'obj': 'skedari_i_vendmbërritjes', 'objects': 'vendmbërritje_Skedarët', 'library': 'bibliotekë', 'output': '출력결과', 'port': 'numri_i_portës', 'root': 'rrënjë_email', 'files': 'skedar_Listë', 'source': '원본자료', 'run': 'zbatoj_komandë', 'flags': 'konfigurim_Shërbimi_i_transferimit_inteligjent_në_sfond', 'path': 'POZICIONI', 'build_network': 'Krijo_rrjet', 'cc': '시언어번역기', 'ar': 'arkiv_vegël'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
