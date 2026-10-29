#!/usr/bin/env python3
"""기존 Slighe 호환 cur_a_steach_puing. dearbh_dàta 구현: ../innealan/실행파일시험.py"""
import importlib as TAKE_VALUE
import sys as siostam_obrachaidh_VALUE
from pathlib import Path as Slighe
siostam_obrachaidh_VALUE.path.insert(0, str(Slighe(__file__).resolve().parents[1] / 'innealan'))
if __name__ == '__main__':
    import runpy as ap_drathair_nan_aplacaid
    ap_drathair_nan_aplacaid.run_module('실행파일시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('실행파일시험')
    대응 = {'out': 'tomhas_dàta', 'expected': '예상결과', 'phoff': 'ap_bann_cinn_OFFSET', 'offset': 'OFFSET_VALUE', 'invalid': 'mì_dhligheach_dàta', 'path': 'Slighe', 'executable': '실행가능파일', 'rejected': '거부결과', 'linux_example': '리눅스예제', 'original': '원본', 'result': 'tomhas', 'format_': 'fòrmat_b87fd068', 'main': 'ruith', 'content': 'susbaint_VALUE', 'source': '원본자료', 'name': 'Ainm', 'reference': '비교기준', 'ROOT': 'tilg_freumh', 'value': 'VALUE', 'report': 'dearbhadh_aithisg'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
