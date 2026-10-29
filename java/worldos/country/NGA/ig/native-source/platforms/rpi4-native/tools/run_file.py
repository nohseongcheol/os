#!/usr/bin/env python3
"""기존 ụzọ_ozi 호환 ndebà_akara. ǹdịnezie_datà 구현: ../Ngwaọrụ/mee_ọbọakwụkwọ.py"""
import importlib as 가져오기
import sys as OS_valuu
from pathlib import Path as ụzọ_ozi
OS_valuu.path.insert(0, str(ụzọ_ozi(__file__).resolve().parents[1] / 'Ngwaọrụ'))
if __name__ == '__main__':
    import runpy as app_ihengosi_ndi_app
    app_ihengosi_ndi_app.run_module('mee_ọbọakwụkwọ', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('mee_ọbọakwụkwọ')
    대응 = {'timeout': '시간제한', 's': 'ùsòròokwū_datà', 'i': '순번', 'match': '일치', 'files': 'ọbọakwụkwọ_ndepụta', 'program': 'app', 'executable': '실행가능파일', 'args': 'agụment_MKPOKỌTA', 'chunk': '조각', 'data': 'datà', 'proc': 'ùsòrò', 'send': 'zìga', 'main': 'Bido', 'marker': '확인표시', 'command': 'Ntiiwu', 'include': '포함항목', 'dumped': '갈무리자료', 'run': 'mee_nnyemiwu', 'p': '자료위치', 'parser': '인수해석기', 'options': 'Ihenhọrọga', 'kind': 'otu_valuu_4b6d6445', 'selector': 'ihe_nhọpụta', 'upload_data': 'bùlie_datà', 'end': 'mèdebe_Nnokwata', 'n': '개수', 'd': 'ebemwèga_datà', 'key': '누름값', 'output': '출력결과', 'line': 'ahịrī', 'name': 'Aha', 'upload_name': 'bùlie_akara_ahà', 'receive': '수신하기'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
