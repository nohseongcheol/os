#!/usr/bin/env python3
"""기존 path 호환 pagpasok_point. totoo_data 구현: ../Mga_Tool/Mag_execute_utos.py"""
import importlib as TAKE_VALUE
import sys as operating_system_VALUE
from pathlib import Path as path
operating_system_VALUE.path.insert(0, str(path(__file__).resolve().parents[1] / 'Mga_Tool'))
if __name__ == '__main__':
    import runpy as app_launcher
    app_launcher.run_module('Mag_execute_utos', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('Mag_execute_utos')
    대응 = {'supported': '지원목록', 'parser': 'parser', 'qemu': '모의기계', 'run_desktop': 'run_desktop', 'main': 'run', 'host': 'host', 'status': 'katayuan_VALUE', 'NetworkBridge': 'Network_bridge', 'ROOT': 'Project_root', 'bridge': 'bridge', 'loader': '적재기', 'base': 'wallpaper_VALUE', 'options': 'Mga_Opsyon', 'binary': 'binary', 'args': 'argumento_ARRAY', 'command': 'utos'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
