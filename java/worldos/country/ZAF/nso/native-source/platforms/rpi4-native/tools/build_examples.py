#!/usr/bin/env python3
"""기존 Tsejana 호환 go_tsenya_tshedimošo_ntlha. kgonthe_data 구현: ../Ditholosi/예제빌드.py"""
import importlib as 가져오기
import sys as tshepedišotirišo_boleng
from pathlib import Path as Tsejana
tshepedišotirišo_boleng.path.insert(0, str(Tsejana(__file__).resolve().parents[1] / 'Ditholosi'))
if __name__ == '__main__':
    import runpy as tirišo_sethala_tirišo
    tirišo_sethala_tirišo.run_module('예제빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제빌드')
    대응 = {'out': '결과자료', 'build_examples': '예제만들기', 'files': 'faele_Lenaneo', 'java': '자바실행', 'run': 'phethagatša_taelo', 'path': 'Tsejana', 'p': '자료위치', 'readme': 'faele_ya_MPALE', 'build_java_library': '자바라이브러리만들기', 'code': 'taelo_TATELANO', 'index': '색인', 'classes': 'legoro_tsela', 'repo': '저장소경로', 'root': '뿌리주소', 'content': 'Diteng_boleng', 'source': '원본자료', 'name': 'Leina', 'target': 'nepo', 'manifest': '꾸러미명세', 'language': 'Polelo'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
