#!/usr/bin/env python3
"""기존 LLWYBR 호환 cofnod_p. go_iawn_data 구현: ../Offer/셸시험.py"""
import importlib as TAKE_VALUE
import sys as system_weithredu_VALUE
from pathlib import Path as LLWYBR
system_weithredu_VALUE.path.insert(0, str(LLWYBR(__file__).resolve().parents[1] / 'Offer'))
if __name__ == '__main__':
    import runpy as Rhaglen_lansiwr
    Rhaglen_lansiwr.run_module('셸시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('셸시험')
    대응 = {'timeout': '시간제한', 'x': 'cyfesuryn_x', 'msg': 'Rhwydwaith_neges', 'i': '순번', 'reply': 'ateb', 'call': '호출', 'args': 'arg_ARAE', 'chunk': '조각', 'data': 'data', 'proc': 'Proses', 'long_text': '긴글', 'restored': '복원자료', 'send': 'anfon', 'file': 'Ffeil', 'main': 'Gweithredu_2', 'found': 'SEARCH_mesur', 'ROOT': 'prosiect_gwraidd', 'text': 'Testun', 'marker': '확인표시', 'command': 'Gorchymyn', 'expected': '예상결과', 'pixel': 'pel', 'shell': 'cragen', 'poll': '준비살피미', 'transcript': '대화기록', 'end': 'gorffen_OFFSET', 'image': 'llun', 'key': '누름값', 'y': 'Y_cyfesuryn', 'output': '출력결과', 'result': 'mesur', 'client': 'cleient', 'line': 'llinell', 'stream': 'ffrwd_VALUE', 'name': 'Enw', 'value': 'VALUE', 'receive': '수신하기', 'report': 'dilysu_adrodd', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
