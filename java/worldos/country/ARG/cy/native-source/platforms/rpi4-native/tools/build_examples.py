#!/usr/bin/env python3
"""기존 LLWYBR 호환 cofnod_p. go_iawn_data 구현: ../Offer/예제빌드.py"""
import importlib as TAKE_VALUE
import sys as system_weithredu_VALUE
from pathlib import Path as LLWYBR
system_weithredu_VALUE.path.insert(0, str(LLWYBR(__file__).resolve().parents[1] / 'Offer'))
if __name__ == '__main__':
    import runpy as Rhaglen_lansiwr
    Rhaglen_lansiwr.run_module('예제빌드', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('예제빌드')
    대응 = {'out': 'mesur_data', 'build_examples': '예제만들기', 'files': 'ffeil_Rhestr', 'java': '자바실행', 'run': 'Gweithredu_gorchymyn', 'path': 'LLWYBR', 'p': 'data_safle', 'readme': 'GWYBODAETH', 'build_java_library': '자바라이브러리만들기', 'code': 'cyfarwyddyd_SEQUENCE', 'index': 'LOOKUP_INDEX', 'classes': 'Dosbarth_llwybr', 'repo': '저장소경로', 'root': 'gwraidd_ADDRESS', 'content': 'Cynnwys_VALUE', 'source': '원본자료', 'name': 'Enw', 'target': 'targed', 'manifest': '꾸러미명세', 'language': 'Iaith'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
