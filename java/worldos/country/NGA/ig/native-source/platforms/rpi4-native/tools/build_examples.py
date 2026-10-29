#!/usr/bin/env python3
"""기존 ụzọ_ozi 호환 ndebà_akara. ǹdịnezie_datà 구현: ../Ngwaọrụ/예제빌드.py"""
import importlib as 가져오기
import sys as OS_valuu
from pathlib import Path as ụzọ_ozi
OS_valuu.path.insert(0, str(ụzọ_ozi(__file__).resolve().parents[1] / 'Ngwaọrụ'))
if __name__ == '__main__':
    import runpy as app_ihengosi_ndi_app
    app_ihengosi_ndi_app.run_module('예제빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제빌드')
    대응 = {'out': '결과자료', 'build_examples': '예제만들기', 'files': 'ọbọakwụkwọ_ndepụta', 'java': '자바실행', 'run': 'mee_nnyemiwu', 'path': 'ụzọ_ozi', 'p': '자료위치', 'readme': 'GỤ̀ỌM', 'build_java_library': '자바라이브러리만들기', 'code': 'okwunkụzi_NSOTANSO', 'index': '색인', 'classes': 'klaàsị_ụzọ_ozi', 'repo': '저장소경로', 'root': '뿌리주소', 'content': 'ndịnà_valuu', 'source': '원본자료', 'name': 'Aha', 'target': 'ebenlereanya', 'manifest': '꾸러미명세', 'language': 'Asụsụ'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
