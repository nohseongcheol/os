#!/usr/bin/env python3
"""기존 yol 호환 giriş_noktası. fiili_veri gerçekleme: ../araçlar/한글입력시험.py"""
import importlib as AL_değer
import sys as işletim_sistemi_değer
from pathlib import Path as yol
işletim_sistemi_değer.path.insert(0, str(yol(__file__).resolve().parents[1] / 'araçlar'))
if __name__ == '__main__':
    import runpy as program_Launcher
    program_Launcher.run_module('한글입력시험', run_name='__main__', alter_sys=True)
else:
    gerçekleme = AL_değer.import_module('한글입력시험')
    eşleme_değer = {'expected': '예상결과', 'Keyboard': 'klavye', 'press': 'bas_tuş', 'self': '자신', 'test_modes_repeat_and_commit': 'test_전환반복확정', 'keys': '누름열', 'test_paste_and_unicode': 'test_yapıştırmak_VE_UNICODE', 'data': 'veri', 'key': '누름값', 'send': 'göndermek', 'test_words': 'test_낱말', 'InputTests': '한글입력시험', 'test_backspace': 'test_앞글자지우기', 'symbol': 'simge_değer', 'char': 'karakter_verileri', 'type': 'TÜR_alan'}
    for Önceki_öğe, geçerli_öğe in eşleme_değer.items():
        if hasattr(gerçekleme, geçerli_öğe): globals()[Önceki_öğe] = getattr(gerçekleme, geçerli_öğe)
