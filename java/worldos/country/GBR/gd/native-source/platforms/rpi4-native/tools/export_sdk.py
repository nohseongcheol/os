#!/usr/bin/env python3
"""기존 Slighe 호환 cur_a_steach_puing. dearbh_dàta 구현: ../innealan/개발꾸러미내보내기.py"""
import importlib as TAKE_VALUE
import sys as siostam_obrachaidh_VALUE
from pathlib import Path as Slighe
siostam_obrachaidh_VALUE.path.insert(0, str(Slighe(__file__).resolve().parents[1] / 'innealan'))
if __name__ == '__main__':
    import runpy as ap_drathair_nan_aplacaid
    ap_drathair_nan_aplacaid.run_module('개발꾸러미내보내기', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('개발꾸러미내보내기')
    대응 = {'out': 'tomhas_dàta', 'obj': 'faidhle_uidhe', 'relative': '상대경로', 'compiler_archive': '번역기꾸러미', 'sdk': '개발꾸러미', 'dist': '배포경로', 'archive': 'taisg', 'main': 'ruith', 'posix': '포직스경로', 'files': 'faidhle_Liosta', 'source': '원본자료', 'name': 'Ainm', 'target': 'targaid', 'ROOT': 'tilg_freumh', 'destination': 'ceann_uidhe_dàta_ADDRESS', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
