#!/usr/bin/env python3
"""기존 đườngDẫn 호환 điểmMục. dữLiệuThựcTế phầnCàiĐặt: ../CôngCụ/thửMànLàmViệc.py"""
import importlib as giáTrịThu
import sys as giáTrịHệThốngĐiềuHành
from pathlib import Path as đườngDẫn
giáTrịHệThốngĐiềuHành.path.insert(0, str(đườngDẫn(__file__).resolve().parents[1] / 'CôngCụ'))
if __name__ == '__main__':
    import runpy as TrìnhKhởiChạyChươngTrình
    TrìnhKhởiChạyChươngTrình.run_module('thửMànLàmViệc', run_name='__main__', alter_sys=True)
else:
    phầnCàiĐặt = giáTrịThu.import_module('thửMànLàmViệc')
    giáTrịPhépÁnhXạ = {'x': 'tọaĐộX', 'typing': 'kýTựCóKiểu', 'message': 'vănBảnThôngBáo', 'start': 'chạy', 'down': 'làĐangNhấn', 'exact': 'giáTrịChínhXác', 'i': 'chỉSốThứBậc', 'press': 'phímNhấn', 'rectangles': 'danhSáchCácHìnhChữNhật', 'sym': 'kýHiệu', 'j': 'thứBậcPhíaTrong', 'deadline': 'thờiGianHạnChót', 'proc': 'tiếnTrình', 'data': 'DữLiệu', 'main': 'chạy', 'w': 'giáTrịRộngĐãYêuCầu', 'init': 'giáTrịBanĐầu', 'block': 'khốiDữLiệu', 'ROOT': 'gốcCâyDựÁn', 'text': 'vănBản', 'marker': 'dấuMốc', 'report': 'báoCáoViệcThẩmĐịnh', 'until': 'đếnKhi', 'clipboard': 'giáTrịBảngTạm', 'dst': 'địaChỉĐích', 'seen': 'cácMụcĐãThấy', 'poll': 'bộGiámSátSựSẵnSàng', 'transcript': 'bảnGhiDiễnTiến', 'port': 'sốCổng', 'offset': 'giáTrịĐộLệch', 'h': 'giáTrịCaoĐãYêuCầu', 'src': 'địaChỉNguyênBản', 'event': 'sựKiện', 'encoding': 'bảngMãKýTự', 'size': 'cỡ', 'key': 'giáTrịĐãNhấn', 'pixels': 'danhSáchCácĐiểmẢnh', 'y': 'tọaĐộY', 'output': 'đầuRa', 'symbol': 'giáTrịKýHiệu', 'client': 'máyKhách', 'char': 'dữLiệuKýTự', 'rgb': 'màuRGB'}
    for phầnMụcTrướcĐó, phầnMụcHiệnTại in giáTrịPhépÁnhXạ.items():
        if hasattr(phầnCàiĐặt, phầnMụcHiệnTại): globals()[phầnMụcTrướcĐó] = getattr(phầnCàiĐặt, phầnMụcHiệnTại)
