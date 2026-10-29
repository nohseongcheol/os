#!/usr/bin/env python3
"""기존 đườngDẫn 호환 điểmMục. dữLiệuThựcTế phầnCàiĐặt: ../CôngCụ/thửVỏLệnh.py"""
import importlib as giáTrịThu
import sys as giáTrịHệThốngĐiềuHành
from pathlib import Path as đườngDẫn
giáTrịHệThốngĐiềuHành.path.insert(0, str(đườngDẫn(__file__).resolve().parents[1] / 'CôngCụ'))
if __name__ == '__main__':
    import runpy as TrìnhKhởiChạyChươngTrình
    TrìnhKhởiChạyChươngTrình.run_module('thửVỏLệnh', run_name='__main__', alter_sys=True)
else:
    phầnCàiĐặt = giáTrịThu.import_module('thửVỏLệnh')
    giáTrịPhépÁnhXạ = {'timeout': 'hếtGiờViệcThựcThi', 'x': 'tọaĐộX', 'msg': 'thôngĐiệpMạng', 'i': 'chỉSốThứBậc', 'reply': 'lờiĐáp', 'call': 'gọiThựcHiện', 'args': 'mảngĐốiSố', 'chunk': 'giáTrịĐoạn', 'data': 'DữLiệu', 'proc': 'tiếnTrình', 'long_text': 'vănBảnDài', 'restored': 'dữLiệuĐãPhụcHồi', 'send': 'gửi', 'file': 'Tệp', 'main': 'chạy', 'found': 'tìmKiếmKếtQuả', 'ROOT': 'gốcCâyDựÁn', 'text': 'vănBản', 'marker': 'dấuMốc', 'command': 'lệnh', 'expected': 'dựKiến', 'pixel': 'điểmẢnh', 'shell': 'vỏLệnh', 'poll': 'bộGiámSátSựSẵnSàng', 'transcript': 'bảnGhiDiễnTiến', 'end': 'độLệchKếtThúc', 'image': 'ảnh', 'key': 'giáTrịĐãNhấn', 'y': 'tọaĐộY', 'output': 'đầuRa', 'result': 'kếtQuả', 'client': 'máyKhách', 'line': 'dòng', 'stream': 'giáTrịLuồng', 'name': 'tên', 'value': 'giáTrị', 'receive': 'nhậnThôngĐiệp', 'report': 'báoCáoViệcThẩmĐịnh', 'work': 'đườngDẫnĐangLàmViệc', 'qmp': 'kếtNốiĐiềuKhiểnGiảLập'}
    for phầnMụcTrướcĐó, phầnMụcHiệnTại in giáTrịPhépÁnhXạ.items():
        if hasattr(phầnCàiĐặt, phầnMụcHiệnTại): globals()[phầnMụcTrướcĐó] = getattr(phầnCàiĐặt, phầnMụcHiệnTại)
