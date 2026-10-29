#!/usr/bin/env python3
"""기존 გეზი 호환 შენატანი_პტ. რეალური_მონაცემები 구현: ../ხელსაწყოები/ატვირთვა_ფაილები.py"""
import importlib as 가져오기
import sys as ოპერაციული_სისტემა_მნიშვნელობა
from pathlib import Path as გეზი
ოპერაციული_სისტემა_მნიშვნელობა.path.insert(0, str(გეზი(__file__).resolve().parents[1] / 'ხელსაწყოები'))
if __name__ == '__main__':
    import runpy as აპი_გამშვები
    აპი_გამშვები.run_module('ატვირთვა_ფაილები', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ატვირთვა_ფაილები')
    대응 = {'data': 'მონაცემები', 'i': '순번', 'name': 'სახელი', 'c': 'სიმბოლოს_კოდი', 'p': 'მონაცემები_პოზიცია', 'args': 'არგუმენტი_მასივი'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
