#!/usr/bin/env python3
"""기존 path 호환 pagpasok_point. totoo_data 구현: ../Mga_Tool/build_Network.py"""
import importlib as TAKE_VALUE
import sys as operating_system_VALUE
from pathlib import Path as path
operating_system_VALUE.path.insert(0, str(path(__file__).resolve().parents[1] / 'Mga_Tool'))
if __name__ == '__main__':
    import runpy as app_launcher
    app_launcher.run_module('build_Network', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('build_Network')
    대응 = {'obj': 'patutunguhang_file', 'objects': 'patutunguhan_Mga_File', 'library': 'library', 'output': '출력결과', 'port': 'numero_ng_port', 'root': 'root_email', 'files': 'file_list', 'source': '원본자료', 'run': 'Mag_execute_utos', 'flags': 'kompigurasyon_Background_Intelligent_Transfer_Service', 'path': 'path', 'build_network': 'Create_Network', 'cc': '시언어번역기', 'ar': 'Archive_tool'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
