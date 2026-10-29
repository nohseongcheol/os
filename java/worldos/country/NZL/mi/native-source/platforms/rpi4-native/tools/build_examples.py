#!/usr/bin/env python3
"""기존 ara 호환 tāurunga_ira. tūturu_raraunga 구현: ../Ngā_Utauta/예제빌드.py"""
import importlib as TAKE_uara
import sys as pūnaha_mahi_uara
from pathlib import Path as ara
pūnaha_mahi_uara.path.insert(0, str(ara(__file__).resolve().parents[1] / 'Ngā_Utauta'))
if __name__ == '__main__':
    import runpy as kaupapa_pūwhiri_taupānga
    kaupapa_pūwhiri_taupānga.run_module('예제빌드', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_uara.import_module('예제빌드')
    대응 = {'out': 'mēhua_raraunga', 'build_examples': '예제만들기', 'files': 'kōnae_Rārangi', 'java': '자바실행', 'run': 'kawe_tono', 'path': 'ara', 'p': 'raraunga_tūranga', 'readme': 'PĀNUIMAI', 'build_java_library': '자바라이브러리만들기', 'code': 'tohutohu_SEQUENCE', 'index': 'Rapu_INDEX', 'classes': 'tauaha_ara', 'repo': '저장소경로', 'root': 'pūtake_ADDRESS', 'content': 'Ihirangi_uara', 'source': '원본자료', 'name': 'Ingoa', 'target': 'ūnga', 'manifest': '꾸러미명세', 'language': 'reo'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
