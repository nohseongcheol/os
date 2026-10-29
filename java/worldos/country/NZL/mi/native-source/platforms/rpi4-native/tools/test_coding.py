#!/usr/bin/env python3
"""기존 ara 호환 tāurunga_ira. tūturu_raraunga 구현: ../Ngā_Utauta/코딩시험.py"""
import importlib as TAKE_uara
import sys as pūnaha_mahi_uara
from pathlib import Path as ara
pūnaha_mahi_uara.path.insert(0, str(ara(__file__).resolve().parents[1] / 'Ngā_Utauta'))
if __name__ == '__main__':
    import runpy as kaupapa_pūwhiri_taupānga
    kaupapa_pūwhiri_taupānga.run_module('코딩시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_uara.import_module('코딩시험')
    대응 = {'out': 'mēhua_raraunga', 'expected': '예상결과', 'sdk': '개발꾸러미', 'suffix': '뒷부분', 'arc': '압축묶음', 'main': 'whakahaere', 'elf': '실행파일', 'run': 'kawe_tono', 'name': 'Ingoa', 'path': 'ara', 'p': 'raraunga_tūranga', 'ROOT': 'whakaatu_pūtake', 'report': 'whakamana_pūrongo', 'args': 'tohenga_HUĀNGA'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
