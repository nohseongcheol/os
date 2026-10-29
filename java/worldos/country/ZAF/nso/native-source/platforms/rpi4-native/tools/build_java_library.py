#!/usr/bin/env python3
"""기존 Tsejana 호환 go_tsenya_tshedimošo_ntlha. kgonthe_data 구현: ../Ditholosi/자바라이브러리빌드.py"""
import importlib as 가져오기
import sys as tshepedišotirišo_boleng
from pathlib import Path as Tsejana
tshepedišotirišo_boleng.path.insert(0, str(Tsejana(__file__).resolve().parents[1] / 'Ditholosi'))
if __name__ == '__main__':
    import runpy as tirišo_sethala_tirišo
    tirišo_sethala_tirišo.run_module('자바라이브러리빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('자바라이브러리빌드')
    대응 = {'header': 'Hlogo_boleng', 'sources': '원문목록', 'i': '순번', 'info': 'msinfo32_exe', 'payload': 'morwalotefelwa_data', 'src': '원본주소', 'run': 'phethagatša_taelo', 'build_java_library': '자바라이브러리만들기', 'relative': '상대경로', 'classes': 'legoro_tsela', 'dist': '배포경로', 'archive': 'Akhaebe', 'output': '출력결과', 'root': '뿌리주소', 'name': 'Leina', 'jar': '자바꾸러미', 'b': '둘째값', 'entries': '항목들'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
