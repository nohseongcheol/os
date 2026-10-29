#!/usr/bin/env python3
"""기존 ọ̀nà 호환 ìgbéwọlé_kókó. gangan_détà 구현: ../Àwọn_irinṣẹ́/fífi_ẹ̀dà_fáìlì_ṣọwọ́_Àwọn_fáìlì.py"""
import importlib as 가져오기
import sys as OS_iye
from pathlib import Path as ọ̀nà
OS_iye.path.insert(0, str(ọ̀nà(__file__).resolve().parents[1] / 'Àwọn_irinṣẹ́'))
if __name__ == '__main__':
    import runpy as àtòjọ_ètò_aṣàfilọ́lẹ̀
    àtòjọ_ètò_aṣàfilọ́lẹ̀.run_module('fífi_ẹ̀dà_fáìlì_ṣọwọ́_Àwọn_fáìlì', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('fífi_ẹ̀dà_fáìlì_ṣọwọ́_Àwọn_fáìlì')
    대응 = {'data': 'détà', 'i': '순번', 'name': 'Orúkọ', 'c': 'kóòdù_ẹyọ_ọ̀rọ̀', 'p': '자료위치', 'args': 'ágúmẹ́ntì_ÀRÉÈ'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
