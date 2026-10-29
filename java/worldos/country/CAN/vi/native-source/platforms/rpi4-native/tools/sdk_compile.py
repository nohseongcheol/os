#!/usr/bin/env python3
"""기존 đườngDẫn 호환 điểmMục. dữLiệuThựcTế phầnCàiĐặt: ../CôngCụ/biênDịchSDK.py"""
import importlib as giáTrịThu
import sys as giáTrịHệThốngĐiềuHành
from pathlib import Path as đườngDẫn
giáTrịHệThốngĐiềuHành.path.insert(0, str(đườngDẫn(__file__).resolve().parents[1] / 'CôngCụ'))
if __name__ == '__main__':
    import runpy as TrìnhKhởiChạyChươngTrình
    TrìnhKhởiChạyChươngTrình.run_module('biênDịchSDK', run_name='__main__', alter_sys=True)
else:
    phầnCàiĐặt = giáTrịThu.import_module('biênDịchSDK')
    giáTrịPhépÁnhXạ = {'compiler': 'côngCụTrìnhBiênDịch', 'obj': 'tệpĐích', 'sdk': 'bộCôngCụPhátTriển', 'output': 'đầuRa', 'main': 'chạy', 'elf': 'tệpTệpThựcThi', 'is_c': 'làNgônNgữC', 'parser': 'bộPhânTích', 'language': 'NgônNgữ', 'work': 'đườngDẫnĐangLàmViệc', 'args': 'mảngĐốiSố'}
    for phầnMụcTrướcĐó, phầnMụcHiệnTại in giáTrịPhépÁnhXạ.items():
        if hasattr(phầnCàiĐặt, phầnMụcHiệnTại): globals()[phầnMụcTrướcĐó] = getattr(phầnCàiĐặt, phầnMụcHiệnTại)
