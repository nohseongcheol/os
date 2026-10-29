#!/usr/bin/env python3
"""기존 POT 호환 vnos_p. dejanski_podatki 구현: ../Orodja/한글입력시험.py"""
import importlib as TAKE_VALUE
import sys as operacijski_sistem_VALUE
from pathlib import Path as POT
operacijski_sistem_VALUE.path.insert(0, str(POT(__file__).resolve().parents[1] / 'Orodja'))
if __name__ == '__main__':
    import runpy as aplikacija_zaganjalnik
    aplikacija_zaganjalnik.run_module('한글입력시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('한글입력시험')
    preslikava_VALUE = {'expected': '예상결과', 'Keyboard': 'tipkovnica', 'press': 'pritisniti_Ključ', 'self': '자신', 'test_modes_repeat_and_commit': 'test_전환반복확정', 'keys': '누름열', 'test_paste_and_unicode': 'preskusiti_prilepiti_AND_UNICODE', 'data': 'podatki', 'key': '누름값', 'send': 'poslati', 'test_words': 'test_낱말', 'InputTests': '한글입력시험', 'test_backspace': 'test_앞글자지우기', 'symbol': 'simbol_VALUE', 'char': 'znakovni_podatki', 'type': 'Tip_območje'}
    for 이전, sprotno_element in preslikava_VALUE.items():
        if hasattr(구현, sprotno_element): globals()[이전] = getattr(구현, sprotno_element)
