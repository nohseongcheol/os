#!/usr/bin/env python3
"""기존 đườngDẫn 호환 điểmMục. dữLiệuThựcTế phầnCàiĐặt: ../CôngCụ/xâyDựngHệThống.py"""
import importlib as giáTrịThu
import sys as giáTrịHệThốngĐiềuHành
from pathlib import Path as đườngDẫn
giáTrịHệThốngĐiềuHành.path.insert(0, str(đườngDẫn(__file__).resolve().parents[1] / 'CôngCụ'))
if __name__ == '__main__':
    import runpy as TrìnhKhởiChạyChươngTrình
    TrìnhKhởiChạyChươngTrình.run_module('xâyDựngHệThống', run_name='__main__', alter_sys=True)
else:
    phầnCàiĐặt = giáTrịThu.import_module('xâyDựngHệThống')
    giáTrịPhépÁnhXạ = {'network': 'mạng', 'BUILD': 'xâyDựngĐườngDẫn', 'ar': 'côngCụKhoLưuTrữ', 'build_examples': 'tạoCácVíDụ', 'posix': 'pOSIX', 'font_data': 'dữLiệuPhôngChữ', 'flags': 'cácBitCấuHình', 'a': 'giáTrịĐầuTiên', 'cc': 'TrìnhBiênDịchC', 'args': 'mảngĐốiSố', 'source_flags': 'cấuHìnhNguyênBản', 'ld': 'côngCụTrìnhLiênKết', 'method': 'mụcPhươngThức', 'main': 'chạy', 'objcopy': 'bộChuyểnĐổiTệpĐốiTượng', 'ROOT': 'gốcCâyDựÁn', 'cxx': 'trìnhBiênDịchCộngCộng', 'includes': 'cóBaoGồm', 'compiler': 'côngCụTrìnhBiênDịch', 'build_users': 'tạoKhôngGianNgườiDùng', 'f': 'mụcTệp', 'extra': 'miềnBổSung', 'exports': 'bảngTraXuất', 'jobs': 'xâyDựngCácCôngViệc', 'run': 'thựcThiLệnh', 'path': 'đườngDẫn', 'REPO': 'gốcCâyKhoNguồn', 'tool': 'CôngCụ', 'classes': 'đườngDẫnLớp', 'output': 'đầuRa', 'samples': 'cácMụcVíDụ', 'symbol': 'giáTrịKýHiệu', 'source': 'dữLiệuNguyênBản', 'name': 'tên', 'build_network': 'tạoMạng', 'font_info': 'thôngTinPhôngChữ', 'manifest': 'bảnKêGóiGộp', 'work': 'đườngDẫnĐangLàmViệc'}
    for phầnMụcTrướcĐó, phầnMụcHiệnTại in giáTrịPhépÁnhXạ.items():
        if hasattr(phầnCàiĐặt, phầnMụcHiệnTại): globals()[phầnMụcTrướcĐó] = getattr(phầnCàiĐặt, phầnMụcHiệnTại)
