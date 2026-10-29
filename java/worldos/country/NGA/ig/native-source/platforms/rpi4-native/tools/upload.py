#!/usr/bin/env python3
"""기존 ụzọ_ozi 호환 ndebà_akara. ǹdịnezie_datà 구현: ../Ngwaọrụ/bùlie_Ndi_ọbọakwụkwọ.py"""
import importlib as 가져오기
import sys as OS_valuu
from pathlib import Path as ụzọ_ozi
OS_valuu.path.insert(0, str(ụzọ_ozi(__file__).resolve().parents[1] / 'Ngwaọrụ'))
if __name__ == '__main__':
    import runpy as app_ihengosi_ndi_app
    app_ihengosi_ndi_app.run_module('bùlie_Ndi_ọbọakwụkwọ', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('bùlie_Ndi_ọbọakwụkwọ')
    대응 = {'data': 'datà', 'i': '순번', 'name': 'Aha', 'c': 'koòdù_nkeakàrà', 'p': '자료위치', 'args': 'agụment_MKPOKỌTA'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
