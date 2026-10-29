#!/usr/bin/env python3
"""기존 გეზი 호환 შენატანი_პტ. რეალური_მონაცემები 구현: ../ხელსაწყოები/აწყობა_ქსელი.py"""
import importlib as 가져오기
import sys as ოპერაციული_სისტემა_მნიშვნელობა
from pathlib import Path as გეზი
ოპერაციული_სისტემა_მნიშვნელობა.path.insert(0, str(გეზი(__file__).resolve().parents[1] / 'ხელსაწყოები'))
if __name__ == '__main__':
    import runpy as აპი_გამშვები
    აპი_გამშვები.run_module('აწყობა_ქსელი', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('აწყობა_ქსელი')
    대응 = {'obj': 'დანიშნულების_ფაილი', 'objects': 'მიმართულება_ფაილები', 'library': 'ბიბლიოთეკა', 'output': '출력결과', 'port': '접속번호', 'root': 'ფესვი_მისამართი', 'files': 'ფაილი_სია', 'source': '원본자료', 'run': 'შესრულება_ბრძანება', 'flags': '설정비트', 'path': 'გეზი', 'build_network': 'შექმნა_ქსელი', 'cc': '시언어번역기', 'ar': 'არქივი_ხელსაწყო'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
