#!/usr/bin/env python3
"""기존 đườngDẫn 호환 điểmMục. dữLiệuThựcTế phầnCàiĐặt: ../CôngCụ/thửJVM.py"""
import importlib as giáTrịThu
import sys as giáTrịHệThốngĐiềuHành
from pathlib import Path as đườngDẫn
giáTrịHệThốngĐiềuHành.path.insert(0, str(đườngDẫn(__file__).resolve().parents[1] / 'CôngCụ'))
if __name__ == '__main__':
    import runpy as TrìnhKhởiChạyChươngTrình
    TrìnhKhởiChạyChươngTrình.run_module('thửJVM', run_name='__main__', alter_sys=True)
else:
    phầnCàiĐặt = giáTrịThu.import_module('thửJVM')
    giáTrịPhépÁnhXạ = {'message': 'vănBảnThôngBáo', 's': 'dữLiệuChuỗi', 'actual': 'kếtQuảThựcTế', 'match': 'làBằng', 'payload': 'dữLiệuNộiTải', 'cases': 'thửTrườngHợp', 'fixture': 'thửDữLiệu', 'main': 'chạy', 'ROOT': 'gốcCâyDựÁn', 'text': 'vănBản', 'valid': 'hợpLệ', 'includes': 'cóBaoGồm', 'include': 'baoGồm', 'expected': 'dựKiến', 'sources': 'DanhSáchMãNguồn', 'tmp': 'đườngDẫnTạm', 'done': 'lượngĐãHoànTất', 'classes': 'đườngDẫnLớp', 'output': 'đầuRa', 'result': 'kếtQuả', 'cmd': 'cácĐốiSốLệnh', 'name': 'tên', 'jar': 'góiGộpJava', 'report': 'báoCáoViệcThẩmĐịnh', 'tests': 'thửDanhSách'}
    for phầnMụcTrướcĐó, phầnMụcHiệnTại in giáTrịPhépÁnhXạ.items():
        if hasattr(phầnCàiĐặt, phầnMụcHiệnTại): globals()[phầnMụcTrướcĐó] = getattr(phầnCàiĐặt, phầnMụcHiệnTại)
