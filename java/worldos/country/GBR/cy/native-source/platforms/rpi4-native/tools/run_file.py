#!/usr/bin/env python3
"""기존 LLWYBR 호환 cofnod_p. go_iawn_data 구현: ../Offer/Gweithredu_ffeil.py"""
import importlib as TAKE_VALUE
import sys as system_weithredu_VALUE
from pathlib import Path as LLWYBR
system_weithredu_VALUE.path.insert(0, str(LLWYBR(__file__).resolve().parents[1] / 'Offer'))
if __name__ == '__main__':
    import runpy as Rhaglen_lansiwr
    Rhaglen_lansiwr.run_module('Gweithredu_ffeil', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('Gweithredu_ffeil')
    대응 = {'timeout': '시간제한', 's': 'testun_data', 'i': '순번', 'match': '일치', 'files': 'ffeil_Rhestr', 'program': 'Rhaglen', 'executable': '실행가능파일', 'args': 'arg_ARAE', 'chunk': '조각', 'data': 'data', 'proc': 'Proses', 'send': 'anfon', 'main': 'Gweithredu_2', 'marker': '확인표시', 'command': 'Gorchymyn', 'include': '포함항목', 'dumped': '갈무리자료', 'run': 'Gweithredu_gorchymyn', 'p': 'data_safle', 'parser': '인수해석기', 'options': 'Dewisiadau', 'kind': 'ardal_VALUE', 'selector': 'dewisydd', 'upload_data': 'Upload_data', 'end': 'gorffen_OFFSET', 'n': 'eitem_COUNT', 'd': 'cyrchfan_data', 'key': '누름값', 'output': '출력결과', 'line': 'llinell', 'name': 'Enw', 'upload_name': 'Upload_enw', 'receive': '수신하기'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
