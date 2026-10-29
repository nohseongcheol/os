#!/usr/bin/env python3
"""기존 aqqut 호환 Iliniku_puinti. taannallarik_titiqqat 구현: ../도구/한글입력시험.py"""
import importlib as 가져오기
import sys as qarasaujakkut_aulattijjut_atuutilik
from pathlib import Path as aqqut
qarasaujakkut_aulattijjut_atuutilik.path.insert(0, str(aqqut(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('한글입력시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('한글입력시험')
    대응 = {'expected': '예상결과', 'Keyboard': 'naqittaut', 'press': '글쇠누르기', 'self': '자신', 'test_modes_repeat_and_commit': 'test_전환반복확정', 'keys': '누름열', 'test_paste_and_unicode': 'test_붙이기유니코드', 'data': 'titiqqat', 'key': '누름값', 'send': 'nassiutili', 'test_words': 'test_낱말', 'InputTests': '한글입력시험', 'test_backspace': 'test_앞글자지우기', 'symbol': '심볼', 'char': 'immikkuuqtuq_titiqqat', 'type': 'qanuittuuninga_Ataqatigiivvik'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
