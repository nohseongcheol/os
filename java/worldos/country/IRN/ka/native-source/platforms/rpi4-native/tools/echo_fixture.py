#!/usr/bin/env python3
"""기존 გეზი 호환 შენატანი_პტ. რეალური_მონაცემები 구현: ../ხელსაწყოები/되돌림시험서버.py"""
import importlib as 가져오기
import sys as ოპერაციული_სისტემა_მნიშვნელობა
from pathlib import Path as გეზი
ოპერაციული_სისტემა_მნიშვნელობა.path.insert(0, str(გეზი(__file__).resolve().parents[1] / 'ხელსაწყოები'))
if __name__ == '__main__':
    import runpy as აპი_გამშვები
    აპი_გამშვები.run_module('되돌림시험서버', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('되돌림시험서버')
    대응 = {'data': 'მონაცემები', 'e': '보조항목', 'connection': 'კავშირი_e05f319b', 'f': 'ფაილი_შენატანი', 'peer': 'კვანძი_მნიშვნელობა_6a3b6fa7', 'self': '자신', 'udp': '전문제어', 't': 'ტერმინალი_შენატანი', 'tcp': 'კავშირი_მართვა', 'EchoFixture': '되돌림시험서버', 'args': 'არგუმენტი_მასივი', 'chunk': '조각'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
