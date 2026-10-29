#!/usr/bin/env python3
"""기존 Slighe 호환 cur_a_steach_puing. dearbh_dàta 구현: ../innealan/자바가상기계시험.py"""
import importlib as TAKE_VALUE
import sys as siostam_obrachaidh_VALUE
from pathlib import Path as Slighe
siostam_obrachaidh_VALUE.path.insert(0, str(Slighe(__file__).resolve().parents[1] / 'innealan'))
if __name__ == '__main__':
    import runpy as ap_drathair_nan_aplacaid
    ap_drathair_nan_aplacaid.run_module('자바가상기계시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('자바가상기계시험')
    대응 = {'message': '알림문', 's': 'sreang_dàta', 'actual': 'dearbh_tomhas', 'match': '일치', 'payload': 'payload_dàta', 'cases': '시험사례', 'fixture': '시험자료', 'main': 'ruith', 'ROOT': 'tilg_freumh', 'text': 'SMS', 'valid': '유효함', 'includes': '포함인수', 'include': '포함항목', 'expected': '예상결과', 'sources': '원문목록', 'tmp': '임시경로', 'done': '완료량', 'classes': 'clas_slighe', 'output': '출력결과', 'result': 'tomhas', 'cmd': '명령인수', 'name': 'Ainm', 'jar': '자바꾸러미', 'report': 'dearbhadh_aithisg', 'tests': '시험목록'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
