#!/usr/bin/env python3
"""기존 SLÓÐ 호환 færsla_P. raun_gögn 구현: ../Verkfæri/셸시험.py"""
import importlib as TAKE_VALUE
import sys as stýrikerfi_VALUE
from pathlib import Path as SLÓÐ
stýrikerfi_VALUE.path.insert(0, str(SLÓÐ(__file__).resolve().parents[1] / 'Verkfæri'))
if __name__ == '__main__':
    import runpy as forrit_ræsir
    forrit_ræsir.run_module('셸시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('셸시험')
    vörpun_VALUE = {'timeout': '시간제한', 'x': 'x_hnit', 'msg': 'Net_skeyti', 'i': '순번', 'reply': 'svara', 'call': '호출', 'args': 'frumbreyta_ARRAY', 'chunk': '조각', 'data': 'gögn', 'proc': 'Ferli', 'long_text': '긴글', 'restored': '복원자료', 'send': 'senda', 'file': 'Skrá', 'main': 'Keyra_2', 'found': 'Leit_mæld_stærð', 'ROOT': 'verk_rót', 'text': 'Texti', 'marker': '확인표시', 'command': 'Skipun', 'expected': '예상결과', 'pixel': 'díll', 'shell': 'skel', 'poll': '준비살피미', 'transcript': '대화기록', 'end': 'ljúka_OFFSET', 'image': 'mynd', 'key': '누름값', 'y': 'Y_hnit', 'output': 'úttak_54cd5e1d', 'result': 'NIÐURSTAÐA', 'client': 'biðlari', 'line': 'Lína', 'stream': 'Stream_VALUE', 'name': 'Heiti', 'value': 'VALUE', 'receive': '수신하기', 'report': 'prófun_skrá', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in vörpun_VALUE.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
