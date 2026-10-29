#!/usr/bin/env python3
"""기존 ọ̀nà 호환 ìgbéwọlé_kókó. gangan_détà 구현: ../Àwọn_irinṣẹ́/흐름시험.py"""
import importlib as 가져오기
import sys as OS_iye
from pathlib import Path as ọ̀nà
OS_iye.path.insert(0, str(ọ̀nà(__file__).resolve().parents[1] / 'Àwọn_irinṣẹ́'))
if __name__ == '__main__':
    import runpy as àtòjọ_ètò_aṣàfilọ́lẹ̀
    àtòjọ_ètò_aṣàfilọ́lẹ̀.run_module('흐름시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('흐름시험')
    대응 = {'out': '결과자료', 'main': 'Rọ́ọ̀nù', 'ROOT': '기준', 'p': '자료위치', 'text': 'SMS', 'report': 'Àfọwọ́sí_ìjábọ̀'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
