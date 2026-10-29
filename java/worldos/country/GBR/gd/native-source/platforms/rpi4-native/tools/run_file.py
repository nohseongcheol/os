#!/usr/bin/env python3
"""기존 Slighe 호환 cur_a_steach_puing. dearbh_dàta 구현: ../innealan/gnìomhaich_faidhle.py"""
import importlib as TAKE_VALUE
import sys as siostam_obrachaidh_VALUE
from pathlib import Path as Slighe
siostam_obrachaidh_VALUE.path.insert(0, str(Slighe(__file__).resolve().parents[1] / 'innealan'))
if __name__ == '__main__':
    import runpy as ap_drathair_nan_aplacaid
    ap_drathair_nan_aplacaid.run_module('gnìomhaich_faidhle', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('gnìomhaich_faidhle')
    대응 = {'timeout': '시간제한', 's': 'sreang_dàta', 'i': '순번', 'match': '일치', 'files': 'faidhle_Liosta', 'program': 'ap', 'executable': '실행가능파일', 'args': 'argamaid_ARRAY', 'chunk': '조각', 'data': 'dàta', 'proc': 'Pròiseas', 'send': 'cuir', 'main': 'ruith', 'marker': '확인표시', 'command': 'àithne', 'include': '포함항목', 'dumped': '갈무리자료', 'run': 'gnìomhaich_àithne', 'p': 'dàta_suidhich', 'parser': '인수해석기', 'options': 'Roghainnean', 'kind': 'roinn_seòrsa_VALUE', 'selector': 'roghnaichear', 'upload_data': 'luchdaich_suas_dàta', 'end': 'crìochnaich_OFFSET', 'n': 'nì_COUNT', 'd': 'ceann_uidhe_dàta', 'key': '누름값', 'output': '출력결과', 'line': 'loidhne', 'name': 'Ainm', 'upload_name': 'luchdaich_suas_ainm', 'receive': '수신하기'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
