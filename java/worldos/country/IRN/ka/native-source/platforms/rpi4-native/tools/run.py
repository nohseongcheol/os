#!/usr/bin/env python3
"""기존 გეზი 호환 შენატანი_პტ. რეალური_მონაცემები 구현: ../ხელსაწყოები/შესრულება_ბრძანება.py"""
import importlib as 가져오기
import sys as ოპერაციული_სისტემა_მნიშვნელობა
from pathlib import Path as გეზი
ოპერაციული_სისტემა_მნიშვნელობა.path.insert(0, str(გეზი(__file__).resolve().parents[1] / 'ხელსაწყოები'))
if __name__ == '__main__':
    import runpy as აპი_გამშვები
    აპი_გამშვები.run_module('შესრულება_ბრძანება', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('შესრულება_ბრძანება')
    대응 = {'supported': '지원목록', 'parser': '인수해석기', 'qemu': '모의기계', 'run_desktop': 'სერია_სამუშაო_დაფა', 'main': 'გაშვება', 'host': 'მასპინძელი', 'status': 'სტატუსი_მნიშვნელობა', 'NetworkBridge': 'ქსელი_ხიდი', 'ROOT': 'პროეცირება_ფესვი', 'bridge': 'ხიდი', 'loader': '적재기', 'base': 'ფონი_მნიშვნელობა', 'options': 'ვარიანტები', 'binary': 'ორობითი', 'args': 'არგუმენტი_მასივი', 'command': 'ბრძანება'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
