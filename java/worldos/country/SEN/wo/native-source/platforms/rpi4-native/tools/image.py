#!/usr/bin/env python3
"""기존 Yoonu_jëmale 호환 dugal_xabaar_Tomb. liteew_mbir 구현: ../Jumtukaay_yi/sos_nataal.py"""
import importlib as 가져오기
import sys as doxalukaay_xëyma
from pathlib import Path as Yoonu_jëmale
doxalukaay_xëyma.path.insert(0, str(Yoonu_jëmale(__file__).resolve().parents[1] / 'Jumtukaay_yi'))
if __name__ == '__main__':
    import runpy as jëfekaay_armuwaaru_jëfekaay
    jëfekaay_armuwaaru_jëfekaay.run_module('sos_nataal', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('sos_nataal')
    대응 = {'total': '총량', 'start': 'daw', 'firmware': '기초제어프로그램', 'files': 'bara_denc_lim', 'archive_base': '압축기준', 'partition': 'Pàccale_bara_denc', 'archive': 'denc', 'main': 'daw', 'block': 'mbir_gatandu', 'ROOT': '기준', 'boot': '부팅경로', 'stage': 'pàcc_xëyma', 'out': '결과자료', 'expected': '예상결과', 'f': 'bara_denc_dugal_xabaar', 'src': '원본주소', 'path': 'Yoonu_jëmale', 'p': '자료위치', 'extracted': '추출자료', 'member': 'Way_bokk', 'mbr': '주부트기록', 'image': 'nataal', 'sector_count': '섹터개수', 'dist': '배포경로', 'sha': '해시계산', 'license_': 'sañ_sañ', 'source': '원본자료', 'name': 'tur_253d1510', 'value': 'xëyma', 'manifest': '꾸러미명세', 'dest': '목적위치', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
