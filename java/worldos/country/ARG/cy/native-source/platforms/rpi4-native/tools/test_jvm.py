#!/usr/bin/env python3
"""기존 LLWYBR 호환 cofnod_p. go_iawn_data 구현: ../Offer/자바가상기계시험.py"""
import importlib as TAKE_VALUE
import sys as system_weithredu_VALUE
from pathlib import Path as LLWYBR
system_weithredu_VALUE.path.insert(0, str(LLWYBR(__file__).resolve().parents[1] / 'Offer'))
if __name__ == '__main__':
    import runpy as Rhaglen_lansiwr
    Rhaglen_lansiwr.run_module('자바가상기계시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('자바가상기계시험')
    대응 = {'message': '알림문', 's': 'testun_data', 'actual': 'go_iawn_mesur', 'match': '일치', 'payload': 'llwyth_uchaf_data', 'cases': '시험사례', 'fixture': '시험자료', 'main': 'Gweithredu_2', 'ROOT': 'prosiect_gwraidd', 'text': 'Testun', 'valid': '유효함', 'includes': '포함인수', 'include': '포함항목', 'expected': '예상결과', 'sources': '원문목록', 'tmp': '임시경로', 'done': '완료량', 'classes': 'Dosbarth_llwybr', 'output': '출력결과', 'result': 'mesur', 'cmd': '명령인수', 'name': 'Enw', 'jar': '자바꾸러미', 'report': 'dilysu_adrodd', 'tests': '시험목록'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
