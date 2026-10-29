#!/usr/bin/env python3
"""기존 Slighe 호환 cur_a_steach_puing. dearbh_dàta 구현: ../innealan/gnìomhaich_àithne.py"""
import importlib as TAKE_VALUE
import sys as siostam_obrachaidh_VALUE
from pathlib import Path as Slighe
siostam_obrachaidh_VALUE.path.insert(0, str(Slighe(__file__).resolve().parents[1] / 'innealan'))
if __name__ == '__main__':
    import runpy as ap_drathair_nan_aplacaid
    ap_drathair_nan_aplacaid.run_module('gnìomhaich_àithne', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('gnìomhaich_àithne')
    대응 = {'supported': '지원목록', 'parser': '인수해석기', 'qemu': '모의기계', 'run_desktop': 'ruith_deasg', 'main': 'ruith', 'host': 'òstair', 'status': 'cor_VALUE', 'NetworkBridge': 'lìonra_drochaid', 'ROOT': 'tilg_freumh', 'bridge': 'drochaid', 'loader': '적재기', 'base': 'cùlaibh_VALUE', 'options': 'Roghainnean', 'binary': 'bìnearaidh', 'args': 'argamaid_ARRAY', 'command': 'àithne'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
