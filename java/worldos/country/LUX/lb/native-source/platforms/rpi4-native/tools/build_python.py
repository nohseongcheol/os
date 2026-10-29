#!/usr/bin/env python3
"""기존 Wee 호환 Agab_Punkt. aktuell_Daten 구현: ../Tools/Build_PYTHON.py"""
import importlib as TAKE_VALUE
import sys as Betribssystem_VALUE
from pathlib import Path as Wee
Betribssystem_VALUE.path.insert(0, str(Wee(__file__).resolve().parents[1] / 'Tools'))
if __name__ == '__main__':
    import runpy as App_App_Beräich
    App_App_Beräich.run_module('Build_PYTHON', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('Build_PYTHON')
    대응 = {'ld': '연결편집기', 'archive': 'Archiv', 'SHA256': 'Validatioun_Hash', 'build_python': 'Create_PYTHON', 'root': 'Racinn_Adress', 'source': '원본자료', 'name': 'Numm', 'path': 'Wee', 'VERSION': '배포판', 'cc': '시언어번역기', 'tar': '타르꾸러미', 'newlib': '뉴리브포함경로', 'member': 'Member'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
