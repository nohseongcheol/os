#!/usr/bin/env python3
"""기존 path 호환 pagpasok_point. totoo_data 구현: ../Mga_Tool/실행파일시험.py"""
import importlib as TAKE_VALUE
import sys as operating_system_VALUE
from pathlib import Path as path
operating_system_VALUE.path.insert(0, str(path(__file__).resolve().parents[1] / 'Mga_Tool'))
if __name__ == '__main__':
    import runpy as app_launcher
    app_launcher.run_module('실행파일시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('실행파일시험')
    대응 = {'out': 'sukat_data', 'expected': '예상결과', 'phoff': 'app_Header_OFFSET', 'offset': 'OFFSET_VALUE', 'invalid': 'hindi_tama_data', 'path': 'path', 'executable': '실행가능파일', 'rejected': '거부결과', 'linux_example': '리눅스예제', 'original': '원본', 'result': 'sukat', 'format_': 'format_b87fd068', 'main': 'run', 'content': 'Nilalaman_VALUE', 'source': '원본자료', 'name': 'pangalan', 'reference': 'Paghahambing_baseline', 'ROOT': 'Project_root', 'value': 'VALUE', 'report': 'pagpapatibay_ulat'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
