#!/usr/bin/env python3
"""기존 გეზი 호환 შენატანი_პტ. რეალური_მონაცემები 구현: ../ხელსაწყოები/შექმნა_ნახატი.py"""
import importlib as 가져오기
import sys as ოპერაციული_სისტემა_მნიშვნელობა
from pathlib import Path as გეზი
ოპერაციული_სისტემა_მნიშვნელობა.path.insert(0, str(გეზი(__file__).resolve().parents[1] / 'ხელსაწყოები'))
if __name__ == '__main__':
    import runpy as აპი_გამშვები
    აპი_გამშვები.run_module('შექმნა_ნახატი', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('შექმნა_ნახატი')
    대응 = {'total': '총량', 'start': 'გაშვება', 'firmware': '기초제어프로그램', 'files': 'ფაილი_სია', 'archive_base': '압축기준', 'partition': 'დანაყოფი_ფაილი', 'archive': 'არქივი', 'main': 'გაშვება', 'block': 'მონაცემები_დაბლოკვა', 'ROOT': 'პროეცირება_ფესვი', 'boot': '부팅경로', 'stage': 'ეტაპი_მნიშვნელობა', 'out': 'გაზომვა_მონაცემები', 'expected': '예상결과', 'f': 'ფაილი_შენატანი', 'src': '원본주소', 'path': 'გეზი', 'p': 'მონაცემები_პოზიცია', 'extracted': '추출자료', 'member': 'წევრი', 'mbr': '주부트기록', 'image': 'ნახატი', 'sector_count': '섹터개수', 'dist': '배포경로', 'sha': '해시계산', 'license_': 'ლიცენზირება', 'source': '원본자료', 'name': 'სახელი', 'value': 'მნიშვნელობა', 'manifest': '꾸러미명세', 'dest': 'მიმართულება_მნიშვნელობა_პოზიცია', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
