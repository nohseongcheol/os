#!/usr/bin/env python3
"""기존 đườngDẫn 호환 điểmMục. dữLiệuThựcTế phầnCàiĐặt: ../CôngCụ/thửCácVíDụ.py"""
import importlib as giáTrịThu
import sys as giáTrịHệThốngĐiềuHành
from pathlib import Path as đườngDẫn
giáTrịHệThốngĐiềuHành.path.insert(0, str(đườngDẫn(__file__).resolve().parents[1] / 'CôngCụ'))
if __name__ == '__main__':
    import runpy as TrìnhKhởiChạyChươngTrình
    TrìnhKhởiChạyChươngTrình.run_module('thửCácVíDụ', run_name='__main__', alter_sys=True)
else:
    phầnCàiĐặt = giáTrịThu.import_module('thửCácVíDụ')
    giáTrịPhépÁnhXạ = {'count': 'sốLượngMục', 'exact': 'giáTrịChínhXác', 'expected_file': 'tệpDựKiến', 'ftp_port': 'sốCổngChuyểnGiaoTệp', 'data': 'DữLiệu', 'graphics_command': 'lệnhĐồHọa', 'main': 'chạy', 'row': 'vịTríHàng', 'init': 'giáTrịBanĐầu', 'target': 'giáTrịĐốiĐích', 'ROOT': 'gốcCâyDựÁn', 'text': 'vănBản', 'binary': 'nhịPhân', 'out': 'dữLiệuKếtQuả', 'entry': 'điểmMục', 'got': 'sốLượngĐãNhận', 'port': 'sốCổng', 'graphics_start': 'bắtChạyBảnVẽ', 'col': 'vịTríCột', 'begin': 'bắtChạyĐộLệch', 'kind': 'giáTrịLoạiMục', 'selector': 'bộChọn', 'n': 'sốLượngPhầnMục', 'key': 'giáTrịĐãNhấn', 'y': 'tọaĐộY', 'client': 'máyKhách', 'line': 'dòng', 'report': 'báoCáoViệcThẩmĐịnh', 'language': 'NgônNgữ', 'x': 'tọaĐộX', 'start': 'chạy', 'rgb': 'màuRGB', 'down': 'làĐangNhấn', 'listing': 'gửiDanhSách', 'payload': 'dữLiệuNộiTải', 'proc': 'tiếnTrình', 'w': 'giáTrịRộngĐãYêuCầu', 'temporary': 'tạm', 'echo': 'mụcMáyChủVọngLại', 'label': 'bảngTraTên', 'content': 'giáTrịNộiDung', 'argument': 'giáTrịĐãChuyểnTiếp', 'EchoServers': 'CácMáyChủVọngLại', 'marker': 'dấuMốc', 'expected': 'dựKiến', 'test_language': 'thửNgônNgữ', 'filename': 'tênMụcTệp', 'shell': 'vỏLệnh', 'color': 'màuĐiểmẢnh', 'transcript': 'bảnGhiDiễnTiến', 'offset': 'giáTrịĐộLệch', 'h': 'giáTrịCaoĐãYêuCầu', 'run': 'thựcThiLệnh', 'c': 'mãKýTự', 'path': 'đườngDẫn', 'encoding': 'bảngMãKýTự', 'end': 'độLệchKếtThúc', 'ftp': 'kếtNốiChuyểnGiaoTệp', 'pixels': 'danhSáchCácĐiểmẢnh', 'symbol': 'giáTrịKýHiệu', 'source': 'dữLiệuNguyênBản', 'name': 'tên', 'receive': 'nhậnThôngĐiệp', 'manifest': 'bảnKêGóiGộp'}
    for phầnMụcTrướcĐó, phầnMụcHiệnTại in giáTrịPhépÁnhXạ.items():
        if hasattr(phầnCàiĐặt, phầnMụcHiệnTại): globals()[phầnMụcTrướcĐó] = getattr(phầnCàiĐặt, phầnMụcHiệnTại)
