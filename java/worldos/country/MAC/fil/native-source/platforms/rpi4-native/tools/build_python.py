#!/usr/bin/env python3
"""기존 path 호환 pagpasok_point. totoo_data 구현: ../Mga_Tool/build_PYTHON.py"""
import importlib as TAKE_VALUE
import sys as operating_system_VALUE
from pathlib import Path as path
operating_system_VALUE.path.insert(0, str(path(__file__).resolve().parents[1] / 'Mga_Tool'))
if __name__ == '__main__':
    import runpy as app_launcher
    app_launcher.run_module('build_PYTHON', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('build_PYTHON')
    대응 = {'ld': '연결편집기', 'archive': 'Archive', 'SHA256': 'pagpapatibay_hash', 'build_python': 'Create_PYTHON', 'root': 'root_email', 'source': '원본자료', 'name': 'pangalan', 'path': 'path', 'VERSION': '배포판', 'cc': '시언어번역기', 'tar': '타르꾸러미', 'newlib': '뉴리브포함경로', 'member': 'miyembro'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
