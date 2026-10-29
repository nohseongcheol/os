#!/usr/bin/env python3
"""기존 يول 호환 كىرگۈزۈش_نوقتا. ھەقىقىي_مەلۇمات 구현: ../قوراللار/قۇرۇش_رەسىم.py"""
import importlib as 가져오기
import sys as مەشغۇلات_سىستېمىسى_قىممىتى
from pathlib import Path as يول
مەشغۇلات_سىستېمىسى_قىممىتى.path.insert(0, str(يول(__file__).resolve().parents[1] / 'قوراللار'))
if __name__ == '__main__':
    import runpy as ئەپ_خادىم
    ئەپ_خادىم.run_module('قۇرۇش_رەسىم', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('قۇرۇش_رەسىم')
    대응 = {'total': '총량', 'start': 'ئىجرا_قىل_2', 'firmware': '기초제어프로그램', 'files': 'ھۆججەت_تىزىم', 'archive_base': '압축기준', 'partition': 'رايون_ھۆججەت', 'archive': 'ئارخىپ', 'main': 'ئىجرا_قىل_2', 'block': 'مەلۇمات_چەكلەش', 'ROOT': 'كۆرسىتىش_يىلتىز', 'boot': '부팅경로', 'stage': 'ئېكران_قىممىتى', 'out': 'ئۆلچەم_مەلۇمات', 'expected': '예상결과', 'f': 'ھۆججەت_كىرگۈزۈش', 'src': '원본주소', 'path': 'يول', 'p': 'مەلۇمات_ئورۇنلاشتۇرۇش', 'extracted': '추출자료', 'member': 'ئەزا', 'mbr': '주부트기록', 'image': 'رەسىم', 'sector_count': '섹터개수', 'dist': '배포경로', 'sha': '해시계산', 'license_': 'ئىجازەت', 'source': '원본자료', 'name': 'ئاتى', 'value': 'قىممىتى', 'manifest': '꾸러미명세', 'dest': 'نىشان_قىممىتى_ئورۇنلاشتۇرۇش', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
