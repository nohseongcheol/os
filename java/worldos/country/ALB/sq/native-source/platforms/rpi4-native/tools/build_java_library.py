#!/usr/bin/env python3
"""기존 POZICIONI 호환 futje_p. aktual_të_dhëna 구현: ../Mjete/자바라이브러리빌드.py"""
import importlib as TAKE_VALUE
import sys as sistem_operativ_VALUE
from pathlib import Path as POZICIONI
sistem_operativ_VALUE.path.insert(0, str(POZICIONI(__file__).resolve().parents[1] / 'Mjete'))
if __name__ == '__main__':
    import runpy as program_hapës
    program_hapës.run_module('자바라이브러리빌드', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('자바라이브러리빌드')
    대응 = {'header': 'Kreu_VALUE', 'sources': '원문목록', 'i': '순번', 'info': 'msinfo32_exe', 'payload': 'ngarkesë_e_dobishme_të_dhëna', 'src': '원본주소', 'run': 'zbatoj_komandë', 'build_java_library': '자바라이브러리만들기', 'relative': '상대경로', 'classes': 'klasë_shteg', 'dist': '배포경로', 'archive': 'arkiv', 'output': '출력결과', 'root': 'rrënjë_email', 'name': 'Emër', 'jar': '자바꾸러미', 'b': 'SECOND_VALUE', 'entries': '항목들'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
