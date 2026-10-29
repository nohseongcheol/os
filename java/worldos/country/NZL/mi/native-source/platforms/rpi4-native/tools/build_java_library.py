#!/usr/bin/env python3
"""기존 ara 호환 tāurunga_ira. tūturu_raraunga 구현: ../Ngā_Utauta/자바라이브러리빌드.py"""
import importlib as TAKE_uara
import sys as pūnaha_mahi_uara
from pathlib import Path as ara
pūnaha_mahi_uara.path.insert(0, str(ara(__file__).resolve().parents[1] / 'Ngā_Utauta'))
if __name__ == '__main__':
    import runpy as kaupapa_pūwhiri_taupānga
    kaupapa_pūwhiri_taupānga.run_module('자바라이브러리빌드', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_uara.import_module('자바라이브러리빌드')
    대응 = {'header': 'Pane_uara', 'sources': '원문목록', 'i': '순번', 'info': 'msinfo32_exe', 'payload': 'tino_raraunga_raraunga', 'src': '원본주소', 'run': 'kawe_tono', 'build_java_library': '자바라이브러리만들기', 'relative': '상대경로', 'classes': 'tauaha_ara', 'dist': '배포경로', 'archive': 'Pūranga', 'output': '출력결과', 'root': 'pūtake_ADDRESS', 'name': 'Ingoa', 'jar': '자바꾸러미', 'b': 'SECOND_uara', 'entries': '항목들'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
