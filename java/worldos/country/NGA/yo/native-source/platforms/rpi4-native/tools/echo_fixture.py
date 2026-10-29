#!/usr/bin/env python3
"""기존 ọ̀nà 호환 ìgbéwọlé_kókó. gangan_détà 구현: ../Àwọn_irinṣẹ́/되돌림시험서버.py"""
import importlib as 가져오기
import sys as OS_iye
from pathlib import Path as ọ̀nà
OS_iye.path.insert(0, str(ọ̀nà(__file__).resolve().parents[1] / 'Àwọn_irinṣẹ́'))
if __name__ == '__main__':
    import runpy as àtòjọ_ètò_aṣàfilọ́lẹ̀
    àtòjọ_ètò_aṣàfilọ́lẹ̀.run_module('되돌림시험서버', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('되돌림시험서버')
    대응 = {'data': 'détà', 'e': '보조항목', 'connection': 'Ìsomọ́_e05f319b', 'f': 'fáìlì_ìgbéwọlé', 'peer': 'ọ̀gbà_iye', 'self': '자신', 'udp': '전문제어', 't': '터미널항목', 'tcp': 'Ìsomọ́_ìdarí', 'EchoFixture': '되돌림시험서버', 'args': 'ágúmẹ́ntì_ÀRÉÈ', 'chunk': '조각'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
