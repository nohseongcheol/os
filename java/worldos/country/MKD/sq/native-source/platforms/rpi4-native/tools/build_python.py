#!/usr/bin/env python3
"""기존 POZICIONI 호환 futje_p. aktual_të_dhëna 구현: ../Mjete/ndërtoj_PYTHON.py"""
import importlib as TAKE_VALUE
import sys as sistem_operativ_VALUE
from pathlib import Path as POZICIONI
sistem_operativ_VALUE.path.insert(0, str(POZICIONI(__file__).resolve().parents[1] / 'Mjete'))
if __name__ == '__main__':
    import runpy as program_hapës
    program_hapës.run_module('ndërtoj_PYTHON', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('ndërtoj_PYTHON')
    대응 = {'ld': '연결편집기', 'archive': 'arkiv', 'SHA256': 'miratim_hash', 'build_python': 'Krijo_PYTHON', 'root': 'rrënjë_email', 'source': '원본자료', 'name': 'Emër', 'path': 'POZICIONI', 'VERSION': '배포판', 'cc': '시언어번역기', 'tar': '타르꾸러미', 'newlib': '뉴리브포함경로', 'member': 'anëtar'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
