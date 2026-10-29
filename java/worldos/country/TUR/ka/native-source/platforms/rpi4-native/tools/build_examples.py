#!/usr/bin/env python3
"""기존 გეზი 호환 შენატანი_პტ. რეალური_მონაცემები 구현: ../ხელსაწყოები/예제빌드.py"""
import importlib as 가져오기
import sys as ოპერაციული_სისტემა_მნიშვნელობა
from pathlib import Path as გეზი
ოპერაციული_სისტემა_მნიშვნელობა.path.insert(0, str(გეზი(__file__).resolve().parents[1] / 'ხელსაწყოები'))
if __name__ == '__main__':
    import runpy as აპი_გამშვები
    აპი_გამშვები.run_module('예제빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제빌드')
    대응 = {'out': 'გაზომვა_მონაცემები', 'build_examples': '예제만들기', 'files': 'ფაილი_სია', 'java': '자바실행', 'run': 'შესრულება_ბრძანება', 'path': 'გეზი', 'p': 'მონაცემები_პოზიცია', 'readme': 'წასაკითხი_ფაილი', 'build_java_library': '자바라이브러리만들기', 'code': '명령열', 'index': 'ძებნა_ინდექსი', 'classes': 'კლასი_მდებარეობა', 'repo': '저장소경로', 'root': 'ფესვი_მისამართი', 'content': 'შიგთავსი_მნიშვნელობა', 'source': '원본자료', 'name': 'სახელი', 'target': 'მიზანი', 'manifest': '꾸러미명세', 'language': 'ენა'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
