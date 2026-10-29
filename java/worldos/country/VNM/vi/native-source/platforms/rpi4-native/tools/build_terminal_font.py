#!/usr/bin/env python3
"""기존 đườngDẫn 호환 điểmMục. dữLiệuThựcTế phầnCàiĐặt: ../CôngCụ/xâyDựngPhôngChữThiếtBịCuối.py"""
import importlib as giáTrịThu
import sys as giáTrịHệThốngĐiềuHành
from pathlib import Path as đườngDẫn
giáTrịHệThốngĐiềuHành.path.insert(0, str(đườngDẫn(__file__).resolve().parents[1] / 'CôngCụ'))
if __name__ == '__main__':
    import runpy as TrìnhKhởiChạyChươngTrình
    TrìnhKhởiChạyChươngTrình.run_module('xâyDựngPhôngChữThiếtBịCuối', run_name='__main__', alter_sys=True)
else:
    phầnCàiĐặt = giáTrịThu.import_module('xâyDựngPhôngChữThiếtBịCuối')
    giáTrịPhépÁnhXạ = {'data': 'DữLiệu', 'img': 'HìnhVẽ', 'bits': 'danhSáchCácBit', 'x': 'tọaĐộX', 'draw': 'vẽMànHình', 'licences': 'cácGiấyPhép', 'paths': 'danhSáchĐườngDẫn', 'y': 'tọaĐộY', 'main': 'chạy', 'src': 'địaChỉNguyênBản', 'fonts': 'danhSáchPhôngChữ', 'ROOT': 'gốcCâyDựÁn', 'p': 'vịTríDữLiệu', 'cp': 'mãHóaKýTự', 'target': 'giáTrịĐốiĐích'}
    for phầnMụcTrướcĐó, phầnMụcHiệnTại in giáTrịPhépÁnhXạ.items():
        if hasattr(phầnCàiĐặt, phầnMụcHiệnTại): globals()[phầnMụcTrướcĐó] = getattr(phầnCàiĐặt, phầnMụcHiệnTại)
