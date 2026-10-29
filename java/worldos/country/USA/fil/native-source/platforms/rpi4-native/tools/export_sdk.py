#!/usr/bin/env python3
"""기존 path 호환 pagpasok_point. totoo_data 구현: ../Mga_Tool/export_SDK.py"""
import importlib as TAKE_VALUE
import sys as operating_system_VALUE
from pathlib import Path as path
operating_system_VALUE.path.insert(0, str(path(__file__).resolve().parents[1] / 'Mga_Tool'))
if __name__ == '__main__':
    import runpy as app_launcher
    app_launcher.run_module('export_SDK', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('export_SDK')
    대응 = {'out': 'sukat_data', 'obj': 'patutunguhang_file', 'relative': '상대경로', 'compiler_archive': '번역기꾸러미', 'sdk': '개발꾸러미', 'dist': '배포경로', 'archive': 'Archive', 'main': 'run', 'posix': '포직스경로', 'files': 'file_list', 'source': '원본자료', 'name': 'pangalan', 'target': 'layunin', 'ROOT': 'Project_root', 'destination': 'patutunguhan_data_email', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
