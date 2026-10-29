#!/usr/bin/env python3
"""기존 đườngDẫn 호환 điểmMục. dữLiệuThựcTế phầnCàiĐặt: ../CôngCụ/xâyDựngMạng.py"""
import importlib as giáTrịThu
import sys as giáTrịHệThốngĐiềuHành
from pathlib import Path as đườngDẫn
giáTrịHệThốngĐiềuHành.path.insert(0, str(đườngDẫn(__file__).resolve().parents[1] / 'CôngCụ'))
if __name__ == '__main__':
    import runpy as TrìnhKhởiChạyChươngTrình
    TrìnhKhởiChạyChươngTrình.run_module('xâyDựngMạng', run_name='__main__', alter_sys=True)
else:
    phầnCàiĐặt = giáTrịThu.import_module('xâyDựngMạng')
    giáTrịPhépÁnhXạ = {'obj': 'tệpĐích', 'objects': 'cácTệpĐích', 'library': 'thưViện', 'output': 'đầuRa', 'port': 'sốCổng', 'root': 'địaChỉGốcCây', 'files': 'danhSáchTệp', 'source': 'dữLiệuNguyênBản', 'run': 'thựcThiLệnh', 'flags': 'cácBitCấuHình', 'path': 'đườngDẫn', 'build_network': 'tạoMạng', 'cc': 'TrìnhBiênDịchC', 'ar': 'côngCụKhoLưuTrữ'}
    for phầnMụcTrướcĐó, phầnMụcHiệnTại in giáTrịPhépÁnhXạ.items():
        if hasattr(phầnCàiĐặt, phầnMụcHiệnTại): globals()[phầnMụcTrướcĐó] = getattr(phầnCàiĐặt, phầnMụcHiệnTại)
