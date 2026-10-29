#!/usr/bin/env python3
"""기존 LLWYBR 호환 cofnod_p. go_iawn_data 구현: ../Offer/실행파일시험.py"""
import importlib as TAKE_VALUE
import sys as system_weithredu_VALUE
from pathlib import Path as LLWYBR
system_weithredu_VALUE.path.insert(0, str(LLWYBR(__file__).resolve().parents[1] / 'Offer'))
if __name__ == '__main__':
    import runpy as Rhaglen_lansiwr
    Rhaglen_lansiwr.run_module('실행파일시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('실행파일시험')
    대응 = {'out': 'mesur_data', 'expected': '예상결과', 'phoff': 'Rhaglen_Pennyn_OFFSET', 'offset': 'OFFSET_VALUE', 'invalid': 'annilys_data', 'path': 'LLWYBR', 'executable': '실행가능파일', 'rejected': '거부결과', 'linux_example': '리눅스예제', 'original': '원본', 'result': 'mesur', 'format_': 'fformat_b87fd068', 'main': 'Gweithredu_2', 'content': 'Cynnwys_VALUE', 'source': '원본자료', 'name': 'Enw', 'reference': '비교기준', 'ROOT': 'prosiect_gwraidd', 'value': 'VALUE', 'report': 'dilysu_adrodd'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
