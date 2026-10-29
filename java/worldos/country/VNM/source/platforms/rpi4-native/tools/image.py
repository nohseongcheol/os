#!/usr/bin/env python3
"""기존 đườngDẫn 호환 điểmMục. dữLiệuThựcTế phầnCàiĐặt: ../CôngCụ/tạoẢnh.py"""
import importlib as giáTrịThu
import sys as giáTrịHệThốngĐiềuHành
from pathlib import Path as đườngDẫn
giáTrịHệThốngĐiềuHành.path.insert(0, str(đườngDẫn(__file__).resolve().parents[1] / 'CôngCụ'))
if __name__ == '__main__':
    import runpy as TrìnhKhởiChạyChươngTrình
    TrìnhKhởiChạyChươngTrình.run_module('tạoẢnh', run_name='__main__', alter_sys=True)
else:
    phầnCàiĐặt = giáTrịThu.import_module('tạoẢnh')
    giáTrịPhépÁnhXạ = {'total': 'sứcChứaTổngCộng', 'start': 'chạy', 'firmware': 'giáTrịPhầnSụn', 'files': 'danhSáchTệp', 'archive_base': 'cơSởKhoLưuTrữ', 'partition': 'tệpPhânVùng', 'archive': 'khoLưuTrữ', 'main': 'chạy', 'block': 'khốiDữLiệu', 'ROOT': 'gốcCâyDựÁn', 'boot': 'đườngDẫnKhởiĐộng', 'stage': 'giáTrịGiaiĐoạn', 'out': 'dữLiệuKếtQuả', 'expected': 'dựKiến', 'f': 'mụcTệp', 'src': 'địaChỉNguyênBản', 'path': 'đườngDẫn', 'p': 'vịTríDữLiệu', 'extracted': 'đãTríchXuất', 'member': 'thànhViên', 'mbr': 'BảnGhiKhởiĐộngChủĐạo', 'image': 'ảnh', 'sector_count': 'sốLượngCungTừ', 'dist': 'đườngDẫnBảnPhânPhối', 'sha': 'tínhMãBăm', 'license_': 'giấyPhép', 'source': 'dữLiệuNguyênBản', 'name': 'tên', 'value': 'giáTrị', 'manifest': 'bảnKêGóiGộp', 'dest': 'vịTríGiáTrịĐích', 'work': 'đườngDẫnĐangLàmViệc'}
    for phầnMụcTrướcĐó, phầnMụcHiệnTại in giáTrịPhépÁnhXạ.items():
        if hasattr(phầnCàiĐặt, phầnMụcHiệnTại): globals()[phầnMụcTrướcĐó] = getattr(phầnCàiĐặt, phầnMụcHiệnTại)
