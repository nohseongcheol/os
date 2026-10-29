#!/usr/bin/env python3
"""기존 გეზი 호환 შენატანი_პტ. რეალური_მონაცემები 구현: ../ხელსაწყოები/실행파일시험.py"""
import importlib as 가져오기
import sys as ოპერაციული_სისტემა_მნიშვნელობა
from pathlib import Path as გეზი
ოპერაციული_სისტემა_მნიშვნელობა.path.insert(0, str(გეზი(__file__).resolve().parents[1] / 'ხელსაწყოები'))
if __name__ == '__main__':
    import runpy as აპი_გამშვები
    აპი_გამშვები.run_module('실행파일시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('실행파일시험')
    대응 = {'out': 'გაზომვა_მონაცემები', 'expected': '예상결과', 'phoff': 'აპი_ზედა_კოლონტიტული_ოფსეტი', 'offset': 'ოფსეტი_მნიშვნელობა', 'invalid': 'არასწორი_მონაცემები', 'path': 'გეზი', 'executable': '실행가능파일', 'rejected': '거부결과', 'linux_example': '리눅스예제', 'original': '원본', 'result': 'გაზომვა', 'format_': 'ფორმატი_b87fd068', 'main': 'გაშვება', 'content': 'შიგთავსი_მნიშვნელობა', 'source': '원본자료', 'name': 'სახელი', 'reference': '비교기준', 'ROOT': 'პროეცირება_ფესვი', 'value': 'მნიშვნელობა', 'report': 'გადამოწმება_ანგარიში'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
