#!/usr/bin/env python3
"""기존 path 호환 pagpasok_point. totoo_data 구현: ../Mga_Tool/SDK_bumuo.py"""
import importlib as TAKE_VALUE
import sys as operating_system_VALUE
from pathlib import Path as path
operating_system_VALUE.path.insert(0, str(path(__file__).resolve().parents[1] / 'Mga_Tool'))
if __name__ == '__main__':
    import runpy as app_launcher
    app_launcher.run_module('SDK_bumuo', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('SDK_bumuo')
    대응 = {'compiler': '번역기', 'obj': 'patutunguhang_file', 'sdk': '개발꾸러미', 'output': '출력결과', 'main': 'run', 'elf': '실행파일', 'is_c': '시언어여부', 'parser': 'parser', 'language': 'Wika', 'work': '작업경로', 'args': 'argumento_ARRAY'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
