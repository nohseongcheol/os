#!/usr/bin/env python3
"""기존 Bide_izena 호환 sarrera_p. benetako_datuak 구현: ../Tresnak/eraiki_PYTHON.py"""
import importlib as HARTU_balio
import sys as sistema_eragile_balio
from pathlib import Path as Bide_izena
sistema_eragile_balio.path.insert(0, str(Bide_izena(__file__).resolve().parents[1] / 'Tresnak'))
if __name__ == '__main__':
    import runpy as aplik_abiarazle
    aplik_abiarazle.run_module('eraiki_PYTHON', run_name='__main__', alter_sys=True)
else:
    구현 = HARTU_balio.import_module('eraiki_PYTHON')
    대응 = {'ld': '연결편집기', 'archive': 'artxibo', 'SHA256': 'balidazio_hash', 'build_python': 'sortu_PYTHON', 'root': 'erro_helbide', 'source': '원본자료', 'name': 'Izena', 'path': 'Bide_izena', 'VERSION': '배포판', 'cc': '시언어번역기', 'tar': '타르꾸러미', 'newlib': '뉴리브포함경로', 'member': 'kide'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
