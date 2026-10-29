#!/usr/bin/env python3
"""기존 ụzọ_ozi 호환 ndebà_akara. ǹdịnezie_datà 구현: ../Ngwaọrụ/wue_Netwọọkụ.py"""
import importlib as 가져오기
import sys as OS_valuu
from pathlib import Path as ụzọ_ozi
OS_valuu.path.insert(0, str(ụzọ_ozi(__file__).resolve().parents[1] / 'Ngwaọrụ'))
if __name__ == '__main__':
    import runpy as app_ihengosi_ndi_app
    app_ihengosi_ndi_app.run_module('wue_Netwọọkụ', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('wue_Netwọọkụ')
    대응 = {'obj': 'ọbọakwụkwọ_ebemwèga', 'objects': 'ebemwèga_Ndi_ọbọakwụkwọ', 'library': 'ọbaakwụkwọ', 'output': '출력결과', 'port': '접속번호', 'root': '뿌리주소', 'files': 'ọbọakwụkwọ_ndepụta', 'source': '원본자료', 'run': 'mee_nnyemiwu', 'flags': '설정비트', 'path': 'ụzọ_ozi', 'build_network': 'mepụta_Netwọọkụ', 'cc': '시언어번역기', 'ar': 'ọkpụ_ngwaọrụ'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
