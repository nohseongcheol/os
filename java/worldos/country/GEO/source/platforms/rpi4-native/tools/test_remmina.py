#!/usr/bin/env python3
"""기존 გეზი 호환 შენატანი_პტ. რეალური_მონაცემები 구현: ../ხელსაწყოები/원격한글시험.py"""
import importlib as 가져오기
import sys as ოპერაციული_სისტემა_მნიშვნელობა
from pathlib import Path as გეზი
ოპერაციული_სისტემა_მნიშვნელობა.path.insert(0, str(გეზი(__file__).resolve().parents[1] / 'ხელსაწყოები'))
if __name__ == '__main__':
    import runpy as აპი_გამშვები
    აპი_გამშვები.run_module('원격한글시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('원격한글시험')
    대응 = {'wait': '기다리기', 'typing': '글자입력', 'start': 'გაშვება', 'profile': 'პროფილი', 'focused': 'ფოკუსირებული', 'serial': '직렬입출력', 'keys': '누름열', 'server': 'სერვერი_მნიშვნელობა', 'log': 'ჟურნალი_ჩაწერა', 'args': 'არგუმენტი_მასივი', 'deadline': '마감시각', 'data': 'მონაცემები', 'candidate': '후보', 'logs': '기록들', 'kw': '이름붙인인수', 'number': '수치', 'main': 'გაშვება', 'ready': '준비완료', 'found': 'ძებნა_გაზომვა', 'guest': 'სტუმარი', 'ROOT': 'პროეცირება_ფესვი', 'marker': '확인표시', 'text': 'ტექსტი', 'out': 'გაზომვა_მონაცემები', 'env': '환경', 'f': 'ფაილი_შენატანი', 'port': '접속번호', 'offset': 'ოფსეტი_მნიშვნელობა', 'version': '판번호', 'p': 'მონაცემები_პოზიცია', 'selector': 'სელექტორი', 'xvfb': 'ვირტუალური_ჩვენება', 'display': 'მონიტორი', 'n': '개수', 'key': '누름값', 'processes': '실행과정들', 'rootfs': '뿌리파일계층', 'xdo': '가상입력도구', 'name': 'სახელი', 'window': 'ფანჯარა', 'report': 'გადამოწმება_ანგარიში', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
