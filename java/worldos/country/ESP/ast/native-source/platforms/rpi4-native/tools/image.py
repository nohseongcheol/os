#!/usr/bin/env python3
"""기존 Camín 호환 진입점. 실제 구현: ../도구/영상만들기.py"""
import importlib as 가져오기
import sys as 체계
from pathlib import Path as Camín
체계.path.insert(0, str(Camín(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('영상만들기', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('영상만들기')
    대응 = {'total': '총량', 'start': 'Executar_2', 'firmware': '기초제어프로그램', 'files': '파일목록', 'archive_base': '압축기준', 'partition': '구획파일', 'archive': '압축꾸러미', 'main': 'Executar_2', 'block': '자료덩이', 'ROOT': '기준', 'boot': '부팅경로', 'stage': '단계', 'out': '결과자료', 'expected': '예상결과', 'f': '파일항목', 'src': '원본주소', 'path': 'Camín', 'p': '자료위치', 'extracted': '추출자료', 'member': '구성원', 'mbr': '주부트기록', 'image': '실행영상', 'sector_count': '섹터개수', 'dist': '배포경로', 'sha': '해시계산', 'license_': '이용허락파일', 'source': '원본자료', 'name': 'Nome', 'value': '값', 'manifest': '꾸러미명세', 'dest': '목적위치', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
