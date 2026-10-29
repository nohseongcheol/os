#!/usr/bin/env python3
"""기존 Paad 호환 진입점. 실제 구현: ../도구/한글입력시험.py"""
import importlib as 가져오기
import sys as 체계
from pathlib import Path as Paad
체계.path.insert(0, str(Paad(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('한글입력시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('한글입력시험')
    대응 = {'expected': '예상결과', 'Keyboard': '글쇠판', 'press': '글쇠누르기', 'self': '자신', 'test_modes_repeat_and_commit': 'test_전환반복확정', 'keys': '누름열', 'test_paste_and_unicode': 'test_붙이기유니코드', 'data': '자료', 'key': '누름값', 'send': '보내기', 'test_words': 'test_낱말', 'InputTests': '한글입력시험', 'test_backspace': 'test_앞글자지우기', 'symbol': '심볼', 'char': '글자값', 'type': '유형'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
