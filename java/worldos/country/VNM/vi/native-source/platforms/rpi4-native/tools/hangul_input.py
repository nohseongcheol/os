#!/usr/bin/env python3
"""기존 đườngDẫn 호환 điểmMục. dữLiệuThựcTế phầnCàiĐặt: ../CôngCụ/đầuVàoHangul.py"""
import importlib as giáTrịThu
import sys as giáTrịHệThốngĐiềuHành
from pathlib import Path as đườngDẫn
giáTrịHệThốngĐiềuHành.path.insert(0, str(đườngDẫn(__file__).resolve().parents[1] / 'CôngCụ'))
if __name__ == '__main__':
    import runpy as TrìnhKhởiChạyChươngTrình
    TrìnhKhởiChạyChươngTrình.run_module('đầuVàoHangul', run_name='__main__', alter_sys=True)
else:
    phầnCàiĐặt = giáTrịThu.import_module('đầuVàoHangul')
    giáTrịPhépÁnhXạ = {'old': 'phầnMụcTrướcĐó', 'backspace': 'xóaLùi', 'committed': 'đãChốt', 'KEYS': 'bốTríPhím', 'self': 'giáTrịBảnThân', 'FINALS': 'jamoCuốiCùngPhứcHợp', 'VOWELS': 'jamoỞGiữaPhứcHợp', 'INITIAL': 'bảngTraJamoBanĐầu', 'initial': 'jamoBanĐầu', 'commit': 'phépGhépChốt', 'feed': 'phímCấp', 'vowel': 'jamoỞGiữa', 'Hangul': 'ghépHangul', 'SPLIT': 'táchJamoCuốiCùng', 'final': 'jamoCuốiCùng', 'key': 'giáTrịĐãNhấn', 'send': 'gửi', 'left': 'bênTrái', 'FINAL': 'bảngTraJamoCuốiCùng', 'history': 'lịchSử', 'pair': 'cặpMột', 'char': 'dữLiệuKýTự', 'VOWEL': 'bảngTraJamoỞGiữa', 'right': 'phải', 'value': 'giáTrị', 'text': 'vănBản'}
    for phầnMụcTrướcĐó, phầnMụcHiệnTại in giáTrịPhépÁnhXạ.items():
        if hasattr(phầnCàiĐặt, phầnMụcHiệnTại): globals()[phầnMụcTrướcĐó] = getattr(phầnCàiĐặt, phầnMụcHiệnTại)
