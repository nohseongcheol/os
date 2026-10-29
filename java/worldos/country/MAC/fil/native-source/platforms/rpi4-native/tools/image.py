#!/usr/bin/env python3
"""기존 path 호환 pagpasok_point. totoo_data 구현: ../Mga_Tool/Create_IMAGE.py"""
import importlib as TAKE_VALUE
import sys as operating_system_VALUE
from pathlib import Path as path
operating_system_VALUE.path.insert(0, str(path(__file__).resolve().parents[1] / 'Mga_Tool'))
if __name__ == '__main__':
    import runpy as app_launcher
    app_launcher.run_module('Create_IMAGE', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('Create_IMAGE')
    대응 = {'total': '총량', 'start': 'run', 'firmware': '기초제어프로그램', 'files': 'file_list', 'archive_base': 'Archive_BASE', 'partition': 'partisyon_file', 'archive': 'Archive', 'main': 'run', 'block': 'data_i_block', 'ROOT': 'Project_root', 'boot': '부팅경로', 'stage': 'stage_VALUE', 'out': 'sukat_data', 'expected': '예상결과', 'f': 'file_pagpasok', 'src': '원본주소', 'path': 'path', 'p': 'data_posisyon', 'extracted': '추출자료', 'member': 'miyembro', 'mbr': '주부트기록', 'image': 'IMAGE', 'sector_count': '섹터개수', 'dist': '배포경로', 'sha': '해시계산', 'license_': 'lisensiya', 'source': '원본자료', 'name': 'pangalan', 'value': 'VALUE', 'manifest': '꾸러미명세', 'dest': 'patutunguhan_VALUE_posisyon', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
