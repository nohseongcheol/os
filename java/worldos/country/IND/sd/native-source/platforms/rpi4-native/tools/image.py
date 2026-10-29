#!/usr/bin/env python3
"""기존 راههه 호환 داخلا_هنڌ. اصلي_ڪوائف 구현: ../اوزار/ٺاھيو_نقش.py"""
import importlib as 가져오기
import sys as آپريٽنگ_سسٽم_قدر
from pathlib import Path as راههه
آپريٽنگ_سسٽم_قدر.path.insert(0, str(راههه(__file__).resolve().parents[1] / 'اوزار'))
if __name__ == '__main__':
    import runpy as ائپ_ائپ_ڊرائر
    ائپ_ائپ_ڊرائر.run_module('ٺاھيو_نقش', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ٺاھيو_نقش')
    대응 = {'total': '총량', 'start': 'هلائڻ', 'firmware': '기초제어프로그램', 'files': 'فائل_فهرست', 'archive_base': '압축기준', 'partition': 'ورڇ_فائل', 'archive': 'محفوظ', 'main': 'هلائڻ', 'block': 'ڪوائف_بلاڪ_ڪريو', 'ROOT': '기준', 'boot': '부팅경로', 'stage': 'اسٽيج_قدر', 'out': '결과자료', 'expected': '예상결과', 'f': 'فائل_داخلا', 'src': '원본주소', 'path': 'راههه', 'p': '자료위치', 'extracted': '추출자료', 'member': 'رڪن', 'mbr': '주부트기록', 'image': 'نقش', 'sector_count': '섹터개수', 'dist': '배포경로', 'sha': '해시계산', 'license_': 'لائبريري_20871e58', 'source': '원본자료', 'name': 'نالو', 'value': 'قدر', 'manifest': '꾸러미명세', 'dest': '목적위치', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
