#!/usr/bin/env python3
"""기존 ụzọ_ozi 호환 ndebà_akara. ǹdịnezie_datà 구현: ../Ngwaọrụ/자바라이브러리빌드.py"""
import importlib as 가져오기
import sys as OS_valuu
from pathlib import Path as ụzọ_ozi
OS_valuu.path.insert(0, str(ụzọ_ozi(__file__).resolve().parents[1] / 'Ngwaọrụ'))
if __name__ == '__main__':
    import runpy as app_ihengosi_ndi_app
    app_ihengosi_ndi_app.run_module('자바라이브러리빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('자바라이브러리빌드')
    대응 = {'header': 'isi_valuu', 'sources': '원문목록', 'i': '순번', 'info': 'Ozi_Sistèm', 'payload': 'ebe_mbulingwa_datà', 'src': '원본주소', 'run': 'mee_nnyemiwu', 'build_java_library': '자바라이브러리만들기', 'relative': '상대경로', 'classes': 'klaàsị_ụzọ_ozi', 'dist': '배포경로', 'archive': 'ọkpụ', 'output': '출력결과', 'root': '뿌리주소', 'name': 'Aha', 'jar': '자바꾸러미', 'b': '둘째값', 'entries': '항목들'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
