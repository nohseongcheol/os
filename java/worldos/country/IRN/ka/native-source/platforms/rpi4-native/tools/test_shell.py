#!/usr/bin/env python3
"""기존 გეზი 호환 შენატანი_პტ. რეალური_მონაცემები 구현: ../ხელსაწყოები/셸시험.py"""
import importlib as 가져오기
import sys as ოპერაციული_სისტემა_მნიშვნელობა
from pathlib import Path as გეზი
ოპერაციული_სისტემა_მნიშვნელობა.path.insert(0, str(გეზი(__file__).resolve().parents[1] / 'ხელსაწყოები'))
if __name__ == '__main__':
    import runpy as აპი_გამშვები
    აპი_გამშვები.run_module('셸시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('셸시험')
    대응 = {'timeout': '시간제한', 'x': 'x_კოორდინატა', 'msg': 'ქსელი_წერილი', 'i': '순번', 'reply': 'პასუხი', 'call': '호출', 'args': 'არგუმენტი_მასივი', 'chunk': '조각', 'data': 'მონაცემები', 'proc': 'პროცესი', 'long_text': '긴글', 'restored': '복원자료', 'send': 'გაგზავნა', 'file': 'ფაილი', 'main': 'გაშვება', 'found': 'ძებნა_გაზომვა', 'ROOT': 'პროეცირება_ფესვი', 'text': 'ტექსტი', 'marker': '확인표시', 'command': 'ბრძანება', 'expected': '예상결과', 'pixel': 'პიქსელი', 'shell': 'გარემო', 'poll': '준비살피미', 'transcript': '대화기록', 'end': 'დასასრული_ოფსეტი', 'image': 'ნახატი', 'key': '누름값', 'y': 'Y_ღილაკი_კოორდინატი', 'output': '출력결과', 'result': 'გაზომვა', 'client': 'კლიენტი', 'line': 'ხაზი', 'stream': 'ნაკადი_მნიშვნელობა', 'name': 'სახელი', 'value': 'მნიშვნელობა', 'receive': '수신하기', 'report': 'გადამოწმება_ანგარიში', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
