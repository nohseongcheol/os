#!/usr/bin/env python3
"""기존 Slighe 호환 cur_a_steach_puing. dearbh_dàta 구현: ../innealan/되돌림시험서버.py"""
import importlib as TAKE_VALUE
import sys as siostam_obrachaidh_VALUE
from pathlib import Path as Slighe
siostam_obrachaidh_VALUE.path.insert(0, str(Slighe(__file__).resolve().parents[1] / 'innealan'))
if __name__ == '__main__':
    import runpy as ap_drathair_nan_aplacaid
    ap_drathair_nan_aplacaid.run_module('되돌림시험서버', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('되돌림시험서버')
    대응 = {'data': 'dàta', 'e': '보조항목', 'connection': 'ceangal_e05f319b', 'f': 'faidhle_cur_a_steach', 'peer': 'seise_VALUE', 'self': '자신', 'udp': '전문제어', 't': 'tèirmineal_cur_a_steach', 'tcp': 'ceangal_smachd', 'EchoFixture': '되돌림시험서버', 'args': 'argamaid_ARRAY', 'chunk': '조각'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
