#!/usr/bin/env python3
"""기존 đườngDẫn 호환 điểmMục. dữLiệuThựcTế phầnCàiĐặt: ../CôngCụ/thửĐầuVàoHangul.py"""
import importlib as giáTrịThu
import sys as giáTrịHệThốngĐiềuHành
from pathlib import Path as đườngDẫn
giáTrịHệThốngĐiềuHành.path.insert(0, str(đườngDẫn(__file__).resolve().parents[1] / 'CôngCụ'))
if __name__ == '__main__':
    import runpy as TrìnhKhởiChạyChươngTrình
    TrìnhKhởiChạyChươngTrình.run_module('thửĐầuVàoHangul', run_name='__main__', alter_sys=True)
else:
    phầnCàiĐặt = giáTrịThu.import_module('thửĐầuVàoHangul')
    giáTrịPhépÁnhXạ = {'expected': 'dựKiến', 'Keyboard': 'BànPhím', 'press': 'phímNhấn', 'self': 'giáTrịBảnThân', 'test_modes_repeat_and_commit': 'thửChốtVàLặpLạiCácChếĐộ', 'keys': 'cácPhímĐãNhấn', 'test_paste_and_unicode': 'thửUnicodeVàDán', 'data': 'DữLiệu', 'key': 'giáTrịĐãNhấn', 'send': 'gửi', 'test_words': 'thửCácTừ', 'InputTests': 'thửĐầuVàoHangul', 'test_backspace': 'thửXóaLùi', 'symbol': 'giáTrịKýHiệu', 'char': 'dữLiệuKýTự', 'type': 'loạiMụcKiểu'}
    for phầnMụcTrướcĐó, phầnMụcHiệnTại in giáTrịPhépÁnhXạ.items():
        if hasattr(phầnCàiĐặt, phầnMụcHiệnTại): globals()[phầnMụcTrướcĐó] = getattr(phầnCàiĐặt, phầnMụcHiệnTại)
