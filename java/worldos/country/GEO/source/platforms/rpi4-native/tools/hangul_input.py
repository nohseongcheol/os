#!/usr/bin/env python3
"""기존 გეზი 호환 შენატანი_პტ. რეალური_მონაცემები 구현: ../ხელსაწყოები/한글입력.py"""
import importlib as 가져오기
import sys as ოპერაციული_სისტემა_მნიშვნელობა
from pathlib import Path as გეზი
ოპერაციული_სისტემა_მნიშვნელობა.path.insert(0, str(გეზი(__file__).resolve().parents[1] / 'ხელსაწყოები'))
if __name__ == '__main__':
    import runpy as აპი_გამშვები
    აპი_გამშვები.run_module('한글입력', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('한글입력')
    대응 = {'old': '이전', 'backspace': '앞글자지우기', 'committed': '확정글', 'KEYS': 'კლავიში_განლაგება', 'self': '자신', 'FINALS': '겹끝소리', 'VOWELS': '겹가운뎃소리', 'INITIAL': '첫소리목록', 'initial': '첫소리', 'commit': '조합확정', 'feed': 'არხი_კლავიში', 'vowel': '가운뎃소리', 'Hangul': '한글조합', 'SPLIT': '끝소리가르기', 'final': '끝소리', 'key': '누름값', 'send': 'გაგზავნა', 'left': '왼쪽', 'FINAL': '끝소리목록', 'history': 'ისტორია', 'pair': '한쌍', 'char': 'სიმბოლო_მონაცემები_4d9f8719', 'VOWEL': '가운뎃소리목록', 'right': '오른쪽', 'value': 'მნიშვნელობა', 'text': 'ტექსტი'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
