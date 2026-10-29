#!/usr/bin/env python3
"""기존 đườngDẫn 호환 điểmMục. dữLiệuThựcTế phầnCàiĐặt: ../CôngCụ/xâyDựngCácVíDụ.py"""
import importlib as giáTrịThu
import sys as giáTrịHệThốngĐiềuHành
from pathlib import Path as đườngDẫn
giáTrịHệThốngĐiềuHành.path.insert(0, str(đườngDẫn(__file__).resolve().parents[1] / 'CôngCụ'))
if __name__ == '__main__':
    import runpy as TrìnhKhởiChạyChươngTrình
    TrìnhKhởiChạyChươngTrình.run_module('xâyDựngCácVíDụ', run_name='__main__', alter_sys=True)
else:
    phầnCàiĐặt = giáTrịThu.import_module('xâyDựngCácVíDụ')
    giáTrịPhépÁnhXạ = {'out': 'dữLiệuKếtQuả', 'build_examples': 'tạoCácVíDụ', 'files': 'danhSáchTệp', 'java': 'thựcThiJava', 'run': 'thựcThiLệnh', 'path': 'đườngDẫn', 'p': 'vịTríDữLiệu', 'readme': 'hãyĐọc', 'build_java_library': 'tạoThưViệnJava', 'code': 'dãyChỉLệnh', 'index': 'chỉSốTraCứu', 'classes': 'đườngDẫnLớp', 'repo': 'đườngDẫnKhoNguồn', 'root': 'địaChỉGốcCây', 'content': 'giáTrịNộiDung', 'source': 'dữLiệuNguyênBản', 'name': 'tên', 'target': 'giáTrịĐốiĐích', 'manifest': 'bảnKêGóiGộp', 'language': 'NgônNgữ'}
    for phầnMụcTrướcĐó, phầnMụcHiệnTại in giáTrịPhépÁnhXạ.items():
        if hasattr(phầnCàiĐặt, phầnMụcHiệnTại): globals()[phầnMụcTrướcĐó] = getattr(phầnCàiĐặt, phầnMụcHiệnTại)
