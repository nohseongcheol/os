#!/usr/bin/env python3
"""기존 Slighe 호환 cur_a_steach_puing. dearbh_dàta 구현: ../innealan/tog_lìonra.py"""
import importlib as TAKE_VALUE
import sys as siostam_obrachaidh_VALUE
from pathlib import Path as Slighe
siostam_obrachaidh_VALUE.path.insert(0, str(Slighe(__file__).resolve().parents[1] / 'innealan'))
if __name__ == '__main__':
    import runpy as ap_drathair_nan_aplacaid
    ap_drathair_nan_aplacaid.run_module('tog_lìonra', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('tog_lìonra')
    대응 = {'obj': 'faidhle_uidhe', 'objects': 'ceann_uidhe_faidhlichean', 'library': 'leabhar_lann', 'output': '출력결과', 'port': '접속번호', 'root': 'freumh_ADDRESS', 'files': 'faidhle_Liosta', 'source': '원본자료', 'run': 'gnìomhaich_àithne', 'flags': '설정비트', 'path': 'Slighe', 'build_network': 'Create_lìonra', 'cc': '시언어번역기', 'ar': 'taisg_inneal'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
