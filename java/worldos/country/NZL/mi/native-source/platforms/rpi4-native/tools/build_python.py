#!/usr/bin/env python3
"""기존 ara 호환 tāurunga_ira. tūturu_raraunga 구현: ../Ngā_Utauta/hanga_PYTHON.py"""
import importlib as TAKE_uara
import sys as pūnaha_mahi_uara
from pathlib import Path as ara
pūnaha_mahi_uara.path.insert(0, str(ara(__file__).resolve().parents[1] / 'Ngā_Utauta'))
if __name__ == '__main__':
    import runpy as kaupapa_pūwhiri_taupānga
    kaupapa_pūwhiri_taupānga.run_module('hanga_PYTHON', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_uara.import_module('hanga_PYTHON')
    대응 = {'ld': '연결편집기', 'archive': 'Pūranga', 'SHA256': 'whakamana_hash', 'build_python': 'Waihanga_PYTHON', 'root': 'pūtake_ADDRESS', 'source': '원본자료', 'name': 'Ingoa', 'path': 'ara', 'VERSION': '배포판', 'cc': '시언어번역기', 'tar': '타르꾸러미', 'newlib': '뉴리브포함경로', 'member': 'mema'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
