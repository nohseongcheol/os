#!/usr/bin/env python3
"""기존 SLÓÐ 호환 færsla_P. raun_gögn 구현: ../Verkfæri/keyra_skrá.py"""
import importlib as TAKE_VALUE
import sys as stýrikerfi_VALUE
from pathlib import Path as SLÓÐ
stýrikerfi_VALUE.path.insert(0, str(SLÓÐ(__file__).resolve().parents[1] / 'Verkfæri'))
if __name__ == '__main__':
    import runpy as forrit_ræsir
    forrit_ræsir.run_module('keyra_skrá', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('keyra_skrá')
    vörpun_VALUE = {'timeout': '시간제한', 's': 'strengur_gögn', 'i': '순번', 'match': '일치', 'files': 'skrá_Listi', 'program': 'forrit', 'executable': '실행가능파일', 'args': 'frumbreyta_ARRAY', 'chunk': '조각', 'data': 'gögn', 'proc': 'Ferli', 'send': 'senda', 'main': 'Keyra_2', 'marker': '확인표시', 'command': 'Skipun', 'include': '포함항목', 'dumped': '갈무리자료', 'run': 'keyra_skipun', 'p': 'gögn_staða', 'parser': 'þáttari', 'options': 'valkostir', 'kind': 'tegund_VALUE', 'selector': 'val', 'upload_data': 'hlaða_upp_gögn', 'end': 'ljúka_OFFSET', 'n': 'vara_COUNT', 'd': 'endastaður_gögn', 'key': '누름값', 'output': 'úttak_54cd5e1d', 'line': 'Lína', 'name': 'Heiti', 'upload_name': 'hlaða_upp_heiti', 'receive': '수신하기'}
    for 이전, 현재 in vörpun_VALUE.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
