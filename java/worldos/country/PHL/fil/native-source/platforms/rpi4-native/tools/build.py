#!/usr/bin/env python3
"""기존 path 호환 pagpasok_point. totoo_data 구현: ../Mga_Tool/build_system.py"""
import importlib as TAKE_VALUE
import sys as operating_system_VALUE
from pathlib import Path as path
operating_system_VALUE.path.insert(0, str(path(__file__).resolve().parents[1] / 'Mga_Tool'))
if __name__ == '__main__':
    import runpy as app_launcher
    app_launcher.run_module('build_system', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('build_system')
    대응 = {'network': 'Network', 'BUILD': 'build_path', 'ar': 'Archive_tool', 'build_examples': '예제만들기', 'posix': '포직스경로', 'font_data': 'font_data', 'flags': 'kompigurasyon_Background_Intelligent_Transfer_Service', 'a': '첫째값', 'cc': '시언어번역기', 'args': 'argumento_ARRAY', 'source_flags': '원본설정', 'ld': '연결편집기', 'method': 'pamamaraan_pagpasok', 'main': 'run', 'objcopy': 'bagay_file_converter', 'ROOT': 'Project_root', 'cxx': '시플플번역기', 'includes': '포함인수', 'compiler': '번역기', 'build_users': 'Create_gumagamit_SPACE', 'f': 'file_pagpasok', 'extra': '추가영역', 'exports': 'export_talahanayan', 'jobs': '빌드작업', 'run': 'Mag_execute_utos', 'path': 'path', 'REPO': 'repository_root', 'tool': 'Mga_Tool', 'classes': 'kategorya_path', 'output': '출력결과', 'samples': '예제들', 'symbol': 'simbolo_VALUE', 'source': '원본자료', 'name': 'pangalan', 'build_network': 'Create_Network', 'font_info': 'font_impormasyon', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
