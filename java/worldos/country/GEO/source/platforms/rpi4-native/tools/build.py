#!/usr/bin/env python3
"""기존 გეზი 호환 შენატანი_პტ. რეალური_მონაცემები 구현: ../ხელსაწყოები/აწყობა_სისტემა.py"""
import importlib as 가져오기
import sys as ოპერაციული_სისტემა_მნიშვნელობა
from pathlib import Path as გეზი
ოპერაციული_სისტემა_მნიშვნელობა.path.insert(0, str(გეზი(__file__).resolve().parents[1] / 'ხელსაწყოები'))
if __name__ == '__main__':
    import runpy as აპი_გამშვები
    აპი_გამშვები.run_module('აწყობა_სისტემა', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('აწყობა_სისტემა')
    대응 = {'network': 'ქსელი', 'BUILD': 'აწყობა_მდებარეობა', 'ar': 'არქივი_ხელსაწყო', 'build_examples': '예제만들기', 'posix': '포직스경로', 'font_data': 'შრიფტი_მონაცემები', 'flags': '설정비트', 'a': '첫째값', 'cc': '시언어번역기', 'args': 'არგუმენტი_მასივი', 'source_flags': '원본설정', 'ld': '연결편집기', 'method': 'მეთოდი_შენატანი', 'main': 'გაშვება', 'objcopy': 'ობიექტი_ფაილი_გარდამქმნელი', 'ROOT': 'პროეცირება_ფესვი', 'cxx': '시플플번역기', 'includes': '포함인수', 'compiler': '번역기', 'build_users': 'შექმნა_მომხმარებელი_სივრცე', 'f': 'ფაილი_შენატანი', 'extra': '추가영역', 'exports': 'ექსპორტი_ცხრილი', 'jobs': '빌드작업', 'run': 'შესრულება_ბრძანება', 'path': 'გეზი', 'REPO': '저장소', 'tool': 'ხელსაწყოები', 'classes': 'კლასი_მდებარეობა', 'output': '출력결과', 'samples': '예제들', 'symbol': 'სიმბოლო_მნიშვნელობა', 'source': '원본자료', 'name': 'სახელი', 'build_network': 'შექმნა_ქსელი', 'font_info': 'შრიფტი_ინფო', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
