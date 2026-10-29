#!/usr/bin/env python3
"""기존 path 호환 pagpasok_point. totoo_data 구현: ../Mga_Tool/Mag_execute_file.py"""
import importlib as TAKE_VALUE
import sys as operating_system_VALUE
from pathlib import Path as path
operating_system_VALUE.path.insert(0, str(path(__file__).resolve().parents[1] / 'Mga_Tool'))
if __name__ == '__main__':
    import runpy as app_launcher
    app_launcher.run_module('Mag_execute_file', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('Mag_execute_file')
    대응 = {'timeout': '시간제한', 's': 'string_data', 'i': '순번', 'match': '일치', 'files': 'file_list', 'program': 'app', 'executable': '실행가능파일', 'args': 'argumento_ARRAY', 'chunk': '조각', 'data': 'data', 'proc': 'Proseso', 'send': 'i_email', 'main': 'run', 'marker': '확인표시', 'command': 'utos', 'include': '포함항목', 'dumped': '갈무리자료', 'run': 'Mag_execute_utos', 'p': 'data_posisyon', 'parser': 'parser', 'options': 'Mga_Opsyon', 'kind': 'kategorya_VALUE', 'selector': 'tagapili', 'upload_data': 'upload_data', 'end': 'tapusin_OFFSET', 'n': 'item_COUNT', 'd': 'patutunguhan_data', 'key': '누름값', 'output': '출력결과', 'line': 'linya', 'name': 'pangalan', 'upload_name': 'upload_pangalan', 'receive': '수신하기'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
