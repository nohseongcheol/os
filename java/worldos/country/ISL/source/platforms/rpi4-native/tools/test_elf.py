#!/usr/bin/env python3
"""기존 SLÓÐ 호환 færsla_P. raun_gögn 구현: ../Verkfæri/실행파일시험.py"""
import importlib as TAKE_VALUE
import sys as stýrikerfi_VALUE
from pathlib import Path as SLÓÐ
stýrikerfi_VALUE.path.insert(0, str(SLÓÐ(__file__).resolve().parents[1] / 'Verkfæri'))
if __name__ == '__main__':
    import runpy as forrit_ræsir
    forrit_ræsir.run_module('실행파일시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('실행파일시험')
    vörpun_VALUE = {'out': 'mæld_stærð_gögn', 'expected': '예상결과', 'phoff': 'forrit_Haus_OFFSET', 'offset': 'OFFSET_VALUE', 'invalid': 'ógilt_gögn', 'path': 'SLÓÐ', 'executable': '실행가능파일', 'rejected': '거부결과', 'linux_example': '리눅스예제', 'original': '원본', 'result': 'NIÐURSTAÐA', 'format_': 'snið_b87fd068', 'main': 'Keyra_2', 'content': 'Efni_VALUE', 'source': '원본자료', 'name': 'Heiti', 'reference': 'Samanburður_grunnlína', 'ROOT': 'verk_rót', 'value': 'VALUE', 'report': 'prófun_skrá'}
    for 이전, 현재 in vörpun_VALUE.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
