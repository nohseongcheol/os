#!/usr/bin/env python3
"""기존 laawol 호환 naatnugol_toɓɓere. laatii_keɓe 구현: ../도구/영상만들기.py"""
import importlib as 가져오기
import sys as yuɓɓo_kurdinɗo_njaru
from pathlib import Path as laawol
yuɓɓo_kurdinɗo_njaru.path.insert(0, str(laawol(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('영상만들기', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('영상만들기')
    대응 = {'total': '총량', 'start': 'huutoraade', 'firmware': '기초제어프로그램', 'files': 'fiilde_Doggol', 'archive_base': '압축기준', 'partition': 'dorƴol_fiilde', 'archive': 'ƴeewtirde', 'main': 'huutoraade', 'block': '자료덩이', 'ROOT': '기준', 'boot': '부팅경로', 'stage': '단계', 'out': '결과자료', 'expected': '예상결과', 'f': 'fiilde_naatnugol', 'src': '원본주소', 'path': 'laawol', 'p': '자료위치', 'extracted': '추출자료', 'member': 'tergal', 'mbr': '주부트기록', 'image': 'natal', 'sector_count': '섹터개수', 'dist': '배포경로', 'sha': '해시계산', 'license_': 'jamirol', 'source': '원본자료', 'name': 'innde', 'value': 'njaru', 'manifest': '꾸러미명세', 'dest': '목적위치', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
