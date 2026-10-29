#!/usr/bin/env python3
"""기존 ara 호환 tāurunga_ira. tūturu_raraunga 구현: ../Ngā_Utauta/실행파일시험.py"""
import importlib as TAKE_uara
import sys as pūnaha_mahi_uara
from pathlib import Path as ara
pūnaha_mahi_uara.path.insert(0, str(ara(__file__).resolve().parents[1] / 'Ngā_Utauta'))
if __name__ == '__main__':
    import runpy as kaupapa_pūwhiri_taupānga
    kaupapa_pūwhiri_taupānga.run_module('실행파일시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_uara.import_module('실행파일시험')
    대응 = {'out': 'mēhua_raraunga', 'expected': '예상결과', 'phoff': 'kaupapa_Pane_OFFSET', 'offset': 'OFFSET_uara', 'invalid': 'muhu_raraunga', 'path': 'ara', 'executable': '실행가능파일', 'rejected': '거부결과', 'linux_example': '리눅스예제', 'original': '원본', 'result': 'mēhua', 'format_': 'hōputu_b87fd068', 'main': 'whakahaere', 'content': 'Ihirangi_uara', 'source': '원본자료', 'name': 'Ingoa', 'reference': '비교기준', 'ROOT': 'whakaatu_pūtake', 'value': 'uara', 'report': 'whakamana_pūrongo'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
