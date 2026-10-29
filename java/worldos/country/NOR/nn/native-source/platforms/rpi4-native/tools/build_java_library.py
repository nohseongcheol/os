#!/usr/bin/env python3
"""기존 STIGE 호환 oppføring_p. faktisk_data 구현: ../Verktøy/자바라이브러리빌드.py"""
import importlib as TAKE_VALUE
import sys as operativsystem_VALUE
from pathlib import Path as STIGE
operativsystem_VALUE.path.insert(0, str(STIGE(__file__).resolve().parents[1] / 'Verktøy'))
if __name__ == '__main__':
    import runpy as app_appskuff
    app_appskuff.run_module('자바라이브러리빌드', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('자바라이브러리빌드')
    대응 = {'header': 'hode_VALUE', 'sources': '원문목록', 'i': '순번', 'info': 'msinfo32_exe', 'payload': 'nyttelast_data', 'src': '원본주소', 'run': 'Utfør_kommando', 'build_java_library': '자바라이브러리만들기', 'relative': '상대경로', 'classes': 'time_bane', 'dist': '배포경로', 'archive': 'Arkiv', 'output': '출력결과', 'root': 'rot_ADDRESS', 'name': 'Namn', 'jar': '자바꾸러미', 'b': 'SECOND_VALUE', 'entries': '항목들'}
    for 이전, betalt_vare in 대응.items():
        if hasattr(구현, betalt_vare): globals()[이전] = getattr(구현, betalt_vare)
