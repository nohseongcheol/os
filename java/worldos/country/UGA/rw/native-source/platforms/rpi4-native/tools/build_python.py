#!/usr/bin/env python3
"""기존 Inzira 호환 icyinjizwa_inota. nyakuri_amakurushingiro 구현: ../Ibikoresho/파이썬빌드.py"""
import importlib as 가져오기
import sys as sisitemu_ngengamikorere_agaciro
from pathlib import Path as Inzira
sisitemu_ngengamikorere_agaciro.path.insert(0, str(Inzira(__file__).resolve().parents[1] / 'Ibikoresho'))
if __name__ == '__main__':
    import runpy as porogaramu_umukozi
    porogaramu_umukozi.run_module('파이썬빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('파이썬빌드')
    대응 = {'ld': '연결편집기', 'archive': 'gushyingura', 'SHA256': 'iyemeza_hashi', 'build_python': '파이썬만들기', 'root': '뿌리주소', 'source': '원본자료', 'name': 'Izina', 'path': 'Inzira', 'VERSION': '배포판', 'cc': '시언어번역기', 'tar': '타르꾸러미', 'newlib': '뉴리브포함경로', 'member': 'ugize_itsinda'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
