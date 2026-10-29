#!/usr/bin/env python3
"""기존 đườngDẫn 호환 điểmMục. dữLiệuThựcTế phầnCàiĐặt: ../CôngCụ/xâyDựngThưViệnJava.py"""
import importlib as giáTrịThu
import sys as giáTrịHệThốngĐiềuHành
from pathlib import Path as đườngDẫn
giáTrịHệThốngĐiềuHành.path.insert(0, str(đườngDẫn(__file__).resolve().parents[1] / 'CôngCụ'))
if __name__ == '__main__':
    import runpy as TrìnhKhởiChạyChươngTrình
    TrìnhKhởiChạyChươngTrình.run_module('xâyDựngThưViệnJava', run_name='__main__', alter_sys=True)
else:
    phầnCàiĐặt = giáTrịThu.import_module('xâyDựngThưViệnJava')
    giáTrịPhépÁnhXạ = {'header': 'giáTrịĐầuMục', 'sources': 'DanhSáchMãNguồn', 'i': 'chỉSốThứBậc', 'info': 'thôngTinHệThống', 'payload': 'dữLiệuNộiTải', 'src': 'địaChỉNguyênBản', 'run': 'thựcThiLệnh', 'build_java_library': 'tạoThưViệnJava', 'relative': 'đườngDẫnTươngĐối', 'classes': 'đườngDẫnLớp', 'dist': 'đườngDẫnBảnPhânPhối', 'archive': 'khoLưuTrữ', 'output': 'đầuRa', 'root': 'địaChỉGốcCây', 'name': 'tên', 'jar': 'góiGộpJava', 'b': 'giáTrịThứHai', 'entries': 'danhSáchCácMục'}
    for phầnMụcTrướcĐó, phầnMụcHiệnTại in giáTrịPhépÁnhXạ.items():
        if hasattr(phầnCàiĐặt, phầnMụcHiệnTại): globals()[phầnMụcTrướcĐó] = getattr(phầnCàiĐặt, phầnMụcHiệnTại)
