#!/usr/bin/env python3
"""기존 ọ̀nà 호환 ìgbéwọlé_kókó. gangan_détà 구현: ../Àwọn_irinṣẹ́/자바가상기계시험.py"""
import importlib as 가져오기
import sys as OS_iye
from pathlib import Path as ọ̀nà
OS_iye.path.insert(0, str(ọ̀nà(__file__).resolve().parents[1] / 'Àwọn_irinṣẹ́'))
if __name__ == '__main__':
    import runpy as àtòjọ_ètò_aṣàfilọ́lẹ̀
    àtòjọ_ètò_aṣàfilọ́lẹ̀.run_module('자바가상기계시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('자바가상기계시험')
    대응 = {'message': '알림문', 's': 'fọ́nrán_détà', 'actual': '실제결과', 'match': '일치', 'payload': 'ojúlówó_détà_détà', 'cases': '시험사례', 'fixture': '시험자료', 'main': 'Rọ́ọ̀nù', 'ROOT': '기준', 'text': 'SMS', 'valid': '유효함', 'includes': '포함인수', 'include': '포함항목', 'expected': '예상결과', 'sources': '원문목록', 'tmp': '임시경로', 'done': '완료량', 'classes': 'ọ̀wọ́_ọ̀nà', 'output': '출력결과', 'result': '결과', 'cmd': '명령인수', 'name': 'Orúkọ', 'jar': '자바꾸러미', 'report': 'Àfọwọ́sí_ìjábọ̀', 'tests': '시험목록'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
