#!/usr/bin/env python3
"""기존 path 호환 pagpasok_point. totoo_data 구현: ../Mga_Tool/시언어번역기빌드.py"""
import importlib as TAKE_VALUE
import sys as operating_system_VALUE
from pathlib import Path as path
operating_system_VALUE.path.insert(0, str(path(__file__).resolve().parents[1] / 'Mga_Tool'))
if __name__ == '__main__':
    import runpy as app_launcher
    app_launcher.run_module('시언어번역기빌드', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('시언어번역기빌드')
    대응 = {'out': 'sukat_data', 'builtins': '내장연산', 'header': 'Header_VALUE', 'sdk': '개발꾸러미', 'build_ccompiler': '시언어번역기만들기', 'i': '순번', 'elf': '실행파일', 'run': 'Mag_execute_utos', 'flags': 'kompigurasyon_Background_Intelligent_Transfer_Service', 'path': 'path', 'p': 'data_posisyon', 'cc': '시언어번역기', 'obj': 'patutunguhang_file', 'flag': 'Mga_Setting_VALUE', 'ld': '연결편집기', 'objects': 'patutunguhan_Mga_File', 'repo': 'repository_path', 'v': '임시값', 'upstream': 'upstream', 'root': 'root_email', 'assets': '탑재자료', 'source': '원본자료', 'name': 'pangalan', 'includes': '포함인수'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
