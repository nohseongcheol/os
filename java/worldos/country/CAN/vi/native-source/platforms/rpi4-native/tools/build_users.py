#!/usr/bin/env python3
"""기존 đườngDẫn 호환 điểmMục. dữLiệuThựcTế phầnCàiĐặt: ../CôngCụ/xâyDựngKhôngGianNgườiDùng.py"""
import importlib as giáTrịThu
import sys as giáTrịHệThốngĐiềuHành
from pathlib import Path as đườngDẫn
giáTrịHệThốngĐiềuHành.path.insert(0, str(đườngDẫn(__file__).resolve().parents[1] / 'CôngCụ'))
if __name__ == '__main__':
    import runpy as TrìnhKhởiChạyChươngTrình
    TrìnhKhởiChạyChươngTrình.run_module('xâyDựngKhôngGianNgườiDùng', run_name='__main__', alter_sys=True)
else:
    phầnCàiĐặt = giáTrịThu.import_module('xâyDựngKhôngGianNgườiDùng')
    giáTrịPhépÁnhXạ = {'mode': 'chếĐộPhươngThức', 'header': 'giáTrịĐầuMục', 'i': 'chỉSốThứBậc', 'build_ccompiler': 'tạoTrìnhBiênDịchC', 'ar': 'côngCụKhoLưuTrữ', 'posix': 'pOSIX', 'payload': 'dữLiệuNộiTải', 'flags': 'cácBitCấuHình', 'cases': 'thửTrườngHợp', 'cc': 'TrìnhBiênDịchC', 'data': 'DữLiệu', 'build_java_library': 'tạoThưViệnJava', 'ld': 'côngCụTrìnhLiênKết', 'repo': 'đườngDẫnKhoNguồn', 'build_python': 'tạoPython', 'inc': 'đườngDẫnBaoGồm', 'argument': 'giáTrịĐãChuyểnTiếp', 'text': 'vănBản', 'headers': 'danhSáchĐầuMục', 'cxx': 'trìnhBiênDịchCộngCộng', 'valid': 'hợpLệ', 'build': 'xâyDựng', 'build_users': 'tạoKhôngGianNgườiDùng', 'compiler': 'côngCụTrìnhBiênDịch', 'uzlib': 'uzlib', 'extra': 'miềnBổSung', 'phoff': 'độLệchĐầuMụcChươngTrình', 'offset': 'giáTrịĐộLệch', 'text_address': 'địaChỉLệnh', 'abi': 'ABIGọi', 'assembly': 'hợpNgữ', 'run': 'thựcThiLệnh', 'path': 'đườngDẫn', 'p': 'vịTríDữLiệu', 'changed': 'đãĐổi', 'n': 'sốLượngPhầnMục', 'flag': 'giáTrịCácThiếtLập', 'index': 'chỉSốTraCứu', 'classes': 'đườngDẫnLớp', 'output': 'đầuRa', 'loads': 'cácLầnNạp', 'data_address': 'địaChỉDữLiệu', 'symbol': 'giáTrịKýHiệu', 'root': 'địaChỉGốcCây', 'patches': 'cácChỉnhSửa', 'source': 'dữLiệuNguyênBản', 'sizes': 'cácCỡ', 'blobs': 'cácKhốiNhịPhân', 'name': 'tên', 'value': 'giáTrị', 'fmt': 'địnhDạngDữLiệu', 'work': 'đườngDẫnĐangLàmViệc'}
    for phầnMụcTrướcĐó, phầnMụcHiệnTại in giáTrịPhépÁnhXạ.items():
        if hasattr(phầnCàiĐặt, phầnMụcHiệnTại): globals()[phầnMụcTrướcĐó] = getattr(phầnCàiĐặt, phầnMụcHiệnTại)
