#!/usr/bin/env python3
"""기존 გეზი 호환 შენატანი_პტ. რეალური_მონაცემები 구현: ../ხელსაწყოები/აწყობა_ტერმინალი_შრიფტი.py"""
import importlib as 가져오기
import sys as ოპერაციული_სისტემა_მნიშვნელობა
from pathlib import Path as გეზი
ოპერაციული_სისტემა_მნიშვნელობა.path.insert(0, str(გეზი(__file__).resolve().parents[1] / 'ხელსაწყოები'))
if __name__ == '__main__':
    import runpy as აპი_გამშვები
    აპი_გამშვები.run_module('აწყობა_ტერმინალი_შრიფტი', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('აწყობა_ტერმინალი_შრიფტი')
    대응 = {'data': 'მონაცემები', 'img': 'ნახატი_მნიშვნელობა_c143fe9e', 'bits': '비트들', 'x': 'x_კოორდინატა', 'draw': '화면그리기', 'licences': '이용허락목록', 'paths': 'მდებარეობა_სია', 'y': 'Y_ღილაკი_კოორდინატი', 'main': 'გაშვება', 'src': '원본주소', 'fonts': 'შრიფტი_სია', 'ROOT': 'პროეცირება_ფესვი', 'p': 'მონაცემები_პოზიცია', 'cp': 'სიმბოლო_კოდირება', 'target': 'მიზანი'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
