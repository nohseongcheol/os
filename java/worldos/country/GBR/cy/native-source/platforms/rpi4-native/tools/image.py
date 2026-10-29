#!/usr/bin/env python3
"""기존 LLWYBR 호환 cofnod_p. go_iawn_data 구현: ../Offer/Creu_llun.py"""
import importlib as TAKE_VALUE
import sys as system_weithredu_VALUE
from pathlib import Path as LLWYBR
system_weithredu_VALUE.path.insert(0, str(LLWYBR(__file__).resolve().parents[1] / 'Offer'))
if __name__ == '__main__':
    import runpy as Rhaglen_lansiwr
    Rhaglen_lansiwr.run_module('Creu_llun', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('Creu_llun')
    대응 = {'total': '총량', 'start': 'Gweithredu_2', 'firmware': '기초제어프로그램', 'files': 'ffeil_Rhestr', 'archive_base': 'Archif_BASE', 'partition': 'rhaniad_ffeil', 'archive': 'Archif', 'main': 'Gweithredu_2', 'block': 'data_rhwystro', 'ROOT': 'prosiect_gwraidd', 'boot': '부팅경로', 'stage': 'cam_VALUE', 'out': 'mesur_data', 'expected': '예상결과', 'f': 'ffeil_cofnod', 'src': '원본주소', 'path': 'LLWYBR', 'p': 'data_safle', 'extracted': '추출자료', 'member': 'aelod', 'mbr': '주부트기록', 'image': 'llun', 'sector_count': '섹터개수', 'dist': '배포경로', 'sha': '해시계산', 'license_': 'trwyddedu', 'source': '원본자료', 'name': 'Enw', 'value': 'VALUE', 'manifest': '꾸러미명세', 'dest': 'cyrchfan_VALUE_safle', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
