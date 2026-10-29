#!/usr/bin/env python3
"""기존 path 호환 pagpasok_point. totoo_data 구현: ../Mga_Tool/build_Terminal_font.py"""
import importlib as TAKE_VALUE
import sys as operating_system_VALUE
from pathlib import Path as path
operating_system_VALUE.path.insert(0, str(path(__file__).resolve().parents[1] / 'Mga_Tool'))
if __name__ == '__main__':
    import runpy as app_launcher
    app_launcher.run_module('build_Terminal_font', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('build_Terminal_font')
    대응 = {'data': 'data', 'img': 'iginuhit_VALUE', 'bits': 'Background_Intelligent_Transfer_Service_list', 'x': 'x_coordinate', 'draw': '화면그리기', 'licences': '이용허락목록', 'paths': 'path_list', 'y': 'Y_button_coordinate', 'main': 'run', 'src': '원본주소', 'fonts': 'font_list', 'ROOT': 'Project_root', 'p': 'data_posisyon', 'cp': 'karakter_pag_encode', 'target': 'layunin'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
