#!/usr/bin/env python3
"""기존 ụzọ_ozi 호환 ndebà_akara. ǹdịnezie_datà 구현: ../Ngwaọrụ/되돌림시험서버.py"""
import importlib as 가져오기
import sys as OS_valuu
from pathlib import Path as ụzọ_ozi
OS_valuu.path.insert(0, str(ụzọ_ozi(__file__).resolve().parents[1] / 'Ngwaọrụ'))
if __name__ == '__main__':
    import runpy as app_ihengosi_ndi_app
    app_ihengosi_ndi_app.run_module('되돌림시험서버', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('되돌림시험서버')
    대응 = {'data': 'datà', 'e': '보조항목', 'connection': 'njikọ_e05f319b', 'f': 'ọbọakwụkwọ_ndebà', 'peer': 'ibè_valuu', 'self': '자신', 'udp': '전문제어', 't': '터미널항목', 'tcp': 'njikọ_njizi', 'EchoFixture': '되돌림시험서버', 'args': 'agụment_MKPOKỌTA', 'chunk': '조각'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
