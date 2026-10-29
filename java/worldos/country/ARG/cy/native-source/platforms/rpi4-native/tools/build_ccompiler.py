#!/usr/bin/env python3
"""기존 LLWYBR 호환 cofnod_p. go_iawn_data 구현: ../Offer/시언어번역기빌드.py"""
import importlib as TAKE_VALUE
import sys as system_weithredu_VALUE
from pathlib import Path as LLWYBR
system_weithredu_VALUE.path.insert(0, str(LLWYBR(__file__).resolve().parents[1] / 'Offer'))
if __name__ == '__main__':
    import runpy as Rhaglen_lansiwr
    Rhaglen_lansiwr.run_module('시언어번역기빌드', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('시언어번역기빌드')
    대응 = {'out': 'mesur_data', 'builtins': '내장연산', 'header': 'Pennyn_VALUE', 'sdk': '개발꾸러미', 'build_ccompiler': '시언어번역기만들기', 'i': '순번', 'elf': '실행파일', 'run': 'Gweithredu_gorchymyn', 'flags': '설정비트', 'path': 'LLWYBR', 'p': 'data_safle', 'cc': '시언어번역기', 'obj': 'ffeil_derbyn', 'flag': 'Gosodiadau_VALUE', 'ld': '연결편집기', 'objects': 'cyrchfan_Ffeil', 'repo': '저장소경로', 'v': '임시값', 'upstream': '외부원문', 'root': 'gwraidd_ADDRESS', 'assets': '탑재자료', 'source': '원본자료', 'name': 'Enw', 'includes': '포함인수'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
