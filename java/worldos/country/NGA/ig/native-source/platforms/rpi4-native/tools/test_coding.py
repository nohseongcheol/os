#!/usr/bin/env python3
"""기존 ụzọ_ozi 호환 ndebà_akara. ǹdịnezie_datà 구현: ../Ngwaọrụ/코딩시험.py"""
import importlib as 가져오기
import sys as OS_valuu
from pathlib import Path as ụzọ_ozi
OS_valuu.path.insert(0, str(ụzọ_ozi(__file__).resolve().parents[1] / 'Ngwaọrụ'))
if __name__ == '__main__':
    import runpy as app_ihengosi_ndi_app
    app_ihengosi_ndi_app.run_module('코딩시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('코딩시험')
    대응 = {'out': '결과자료', 'expected': '예상결과', 'sdk': '개발꾸러미', 'suffix': '뒷부분', 'arc': '압축묶음', 'main': 'Bido', 'elf': '실행파일', 'run': 'mee_nnyemiwu', 'name': 'Aha', 'path': 'ụzọ_ozi', 'p': '자료위치', 'ROOT': '기준', 'report': 'nkwèputaonòdù_akụkọ', 'args': 'agụment_MKPOKỌTA'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
