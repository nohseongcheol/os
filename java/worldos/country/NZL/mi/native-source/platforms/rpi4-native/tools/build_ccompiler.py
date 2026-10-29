#!/usr/bin/env python3
"""기존 ara 호환 tāurunga_ira. tūturu_raraunga 구현: ../Ngā_Utauta/시언어번역기빌드.py"""
import importlib as TAKE_uara
import sys as pūnaha_mahi_uara
from pathlib import Path as ara
pūnaha_mahi_uara.path.insert(0, str(ara(__file__).resolve().parents[1] / 'Ngā_Utauta'))
if __name__ == '__main__':
    import runpy as kaupapa_pūwhiri_taupānga
    kaupapa_pūwhiri_taupānga.run_module('시언어번역기빌드', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_uara.import_module('시언어번역기빌드')
    대응 = {'out': 'mēhua_raraunga', 'builtins': '내장연산', 'header': 'Pane_uara', 'sdk': '개발꾸러미', 'build_ccompiler': '시언어번역기만들기', 'i': '순번', 'elf': '실행파일', 'run': 'kawe_tono', 'flags': '설정비트', 'path': 'ara', 'p': 'raraunga_tūranga', 'cc': '시언어번역기', 'obj': 'kōnae_ūnga_ffac9b48', 'flag': 'Ngā_Tautuhinga_uara', 'ld': '연결편집기', 'objects': 'ūnga_Ngā_Kōnae', 'repo': '저장소경로', 'v': '임시값', 'upstream': '외부원문', 'root': 'pūtake_ADDRESS', 'assets': '탑재자료', 'source': '원본자료', 'name': 'Ingoa', 'includes': '포함인수'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
