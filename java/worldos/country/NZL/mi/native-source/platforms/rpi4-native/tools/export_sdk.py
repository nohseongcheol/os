#!/usr/bin/env python3
"""기존 ara 호환 tāurunga_ira. tūturu_raraunga 구현: ../Ngā_Utauta/개발꾸러미내보내기.py"""
import importlib as TAKE_uara
import sys as pūnaha_mahi_uara
from pathlib import Path as ara
pūnaha_mahi_uara.path.insert(0, str(ara(__file__).resolve().parents[1] / 'Ngā_Utauta'))
if __name__ == '__main__':
    import runpy as kaupapa_pūwhiri_taupānga
    kaupapa_pūwhiri_taupānga.run_module('개발꾸러미내보내기', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_uara.import_module('개발꾸러미내보내기')
    대응 = {'out': 'mēhua_raraunga', 'obj': 'kōnae_ūnga_ffac9b48', 'relative': '상대경로', 'compiler_archive': '번역기꾸러미', 'sdk': '개발꾸러미', 'dist': '배포경로', 'archive': 'Pūranga', 'main': 'whakahaere', 'posix': '포직스경로', 'files': 'kōnae_Rārangi', 'source': '원본자료', 'name': 'Ingoa', 'target': 'ūnga', 'ROOT': 'whakaatu_pūtake', 'destination': 'ūnga_raraunga_ADDRESS', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
