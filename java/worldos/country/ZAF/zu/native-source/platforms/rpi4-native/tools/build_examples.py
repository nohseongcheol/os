#!/usr/bin/env python3
"""기존 Indlela_2 호환 okufakwayo_iphoyinti. ulwazi_ngokwenzekile_imininingwane 구현: ../Amathuluzi/예제빌드.py"""
import importlib as 가져오기
import sys as isistimu_yokusebenza_inani
from pathlib import Path as Indlela_2
isistimu_yokusebenza_inani.path.insert(0, str(Indlela_2(__file__).resolve().parents[1] / 'Amathuluzi'))
if __name__ == '__main__':
    import runpy as i_app_ikhabethe_le_app
    i_app_ikhabethe_le_app.run_module('예제빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제빌드')
    대응 = {'out': '결과자료', 'build_examples': '예제만들기', 'files': 'ifayela_Uhlu', 'java': '자바실행', 'run': 'yenza_umyalo', 'path': 'Indlela_2', 'p': '자료위치', 'readme': 'NGIFUNDE', 'build_java_library': '자바라이브러리만들기', 'code': 'umyalelo_UKULANDELANA', 'index': '색인', 'classes': 'uhlobo_umzila', 'repo': '저장소경로', 'root': '뿌리주소', 'content': 'Okuqukethwe_inani', 'source': '원본자료', 'name': 'Igama', 'target': 'impokophelo', 'manifest': '꾸러미명세', 'language': 'Ulimi'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
