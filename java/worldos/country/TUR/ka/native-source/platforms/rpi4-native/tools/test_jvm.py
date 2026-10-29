#!/usr/bin/env python3
"""기존 გეზი 호환 შენატანი_პტ. რეალური_მონაცემები 구현: ../ხელსაწყოები/자바가상기계시험.py"""
import importlib as 가져오기
import sys as ოპერაციული_სისტემა_მნიშვნელობა
from pathlib import Path as გეზი
ოპერაციული_სისტემა_მნიშვნელობა.path.insert(0, str(გეზი(__file__).resolve().parents[1] / 'ხელსაწყოები'))
if __name__ == '__main__':
    import runpy as აპი_გამშვები
    აპი_გამშვები.run_module('자바가상기계시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('자바가상기계시험')
    대응 = {'message': '알림문', 's': 'სტრიქონი_მონაცემები', 'actual': 'რეალური_გაზომვა', 'match': '일치', 'payload': 'დატვირთვა_მონაცემები', 'cases': '시험사례', 'fixture': '시험자료', 'main': 'გაშვება', 'ROOT': 'პროეცირება_ფესვი', 'text': 'ტექსტი', 'valid': '유효함', 'includes': '포함인수', 'include': '포함항목', 'expected': '예상결과', 'sources': '원문목록', 'tmp': '임시경로', 'done': '완료량', 'classes': 'კლასი_მდებარეობა', 'output': '출력결과', 'result': 'გაზომვა', 'cmd': '명령인수', 'name': 'სახელი', 'jar': '자바꾸러미', 'report': 'გადამოწმება_ანგარიში', 'tests': '시험목록'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
