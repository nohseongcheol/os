#!/usr/bin/env python3
"""기존 გეზი 호환 შენატანი_პტ. რეალური_მონაცემები 구현: ../ხელსაწყოები/파이썬빌드.py"""
import importlib as 가져오기
import sys as ოპერაციული_სისტემა_მნიშვნელობა
from pathlib import Path as გეზი
ოპერაციული_სისტემა_მნიშვნელობა.path.insert(0, str(გეზი(__file__).resolve().parents[1] / 'ხელსაწყოები'))
if __name__ == '__main__':
    import runpy as აპი_გამშვები
    აპი_გამშვები.run_module('파이썬빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('파이썬빌드')
    대응 = {'ld': '연결편집기', 'archive': 'არქივი', 'SHA256': 'გადამოწმება_ჰეში', 'build_python': '파이썬만들기', 'root': 'ფესვი_მისამართი', 'source': '원본자료', 'name': 'სახელი', 'path': 'გეზი', 'VERSION': '배포판', 'cc': '시언어번역기', 'tar': '타르꾸러미', 'newlib': '뉴리브포함경로', 'member': 'წევრი'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
