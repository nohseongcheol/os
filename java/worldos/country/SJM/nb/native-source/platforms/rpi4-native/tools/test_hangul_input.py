#!/usr/bin/env python3
"""기존 Sti 호환 inngangspunkt. faktisk_data 구현: ../Verktøy/한글입력시험.py"""
import importlib as TA_VERDI
import sys as operativsystem_VERDI
from pathlib import Path as Sti
operativsystem_VERDI.path.insert(0, str(Sti(__file__).resolve().parents[1] / 'Verktøy'))
if __name__ == '__main__':
    import runpy as app_appskuff
    app_appskuff.run_module('한글입력시험', run_name='__main__', alter_sys=True)
else:
    구현 = TA_VERDI.import_module('한글입력시험')
    tildeling_VERDI = {'expected': '예상결과', 'Keyboard': 'tastatur', 'press': '글쇠누르기', 'self': '자신', 'test_modes_repeat_and_commit': 'test_전환반복확정', 'keys': '누름열', 'test_paste_and_unicode': 'test_lime_inn_OG_UNICODE', 'data': 'data', 'key': '누름값', 'send': 'sende', 'test_words': 'test_낱말', 'InputTests': '한글입력시험', 'test_backspace': 'test_앞글자지우기', 'symbol': 'symbol_VERDI', 'char': 'tegndata', 'type': 'Type_område'}
    for Forrige_vare, betalt_vare in tildeling_VERDI.items():
        if hasattr(구현, betalt_vare): globals()[Forrige_vare] = getattr(구현, betalt_vare)
