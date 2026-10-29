#!/usr/bin/env python3
"""기존 path 호환 pagpasok_point. totoo_data 구현: ../Mga_Tool/예제빌드.py"""
import importlib as TAKE_VALUE
import sys as operating_system_VALUE
from pathlib import Path as path
operating_system_VALUE.path.insert(0, str(path(__file__).resolve().parents[1] / 'Mga_Tool'))
if __name__ == '__main__':
    import runpy as app_launcher
    app_launcher.run_module('예제빌드', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('예제빌드')
    대응 = {'out': 'sukat_data', 'build_examples': '예제만들기', 'files': 'file_list', 'java': '자바실행', 'run': 'Mag_execute_utos', 'path': 'path', 'p': 'data_posisyon', 'readme': 'BASAHINAKO', 'build_java_library': '자바라이브러리만들기', 'code': 'instruksiyon_SEQUENCE', 'index': 'LOOKUP_INDEX', 'classes': 'kategorya_path', 'repo': 'repository_path', 'root': 'root_email', 'content': 'Nilalaman_VALUE', 'source': '원본자료', 'name': 'pangalan', 'target': 'layunin', 'manifest': '꾸러미명세', 'language': 'Wika'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
