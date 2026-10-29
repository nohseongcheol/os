#!/usr/bin/env python3
"""기존 გეზი 호환 შენატანი_პტ. რეალური_მონაცემები 구현: ../ხელსაწყოები/შესრულება_ფაილი.py"""
import importlib as 가져오기
import sys as ოპერაციული_სისტემა_მნიშვნელობა
from pathlib import Path as გეზი
ოპერაციული_სისტემა_მნიშვნელობა.path.insert(0, str(გეზი(__file__).resolve().parents[1] / 'ხელსაწყოები'))
if __name__ == '__main__':
    import runpy as აპი_გამშვები
    აპი_გამშვები.run_module('შესრულება_ფაილი', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('შესრულება_ფაილი')
    대응 = {'timeout': '시간제한', 's': 'სტრიქონი_მონაცემები', 'i': '순번', 'match': '일치', 'files': 'ფაილი_სია', 'program': 'აპი', 'executable': '실행가능파일', 'args': 'არგუმენტი_მასივი', 'chunk': '조각', 'data': 'მონაცემები', 'proc': 'პროცესი', 'send': 'გაგზავნა', 'main': 'გაშვება', 'marker': '확인표시', 'command': 'ბრძანება', 'include': '포함항목', 'dumped': '갈무리자료', 'run': 'შესრულება_ბრძანება', 'p': 'მონაცემები_პოზიცია', 'parser': '인수해석기', 'options': 'ვარიანტები', 'kind': 'კატეგორია_მნიშვნელობა', 'selector': 'სელექტორი', 'upload_data': 'ატვირთვა_მონაცემები', 'end': 'დასასრული_ოფსეტი', 'n': '개수', 'd': 'მიმართულება_მონაცემები', 'key': '누름값', 'output': '출력결과', 'line': 'ხაზი', 'name': 'სახელი', 'upload_name': 'ატვირთვა_სახელი', 'receive': '수신하기'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
