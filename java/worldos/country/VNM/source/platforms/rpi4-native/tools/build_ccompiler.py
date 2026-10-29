#!/usr/bin/env python3
"""기존 đườngDẫn 호환 điểmMục. dữLiệuThựcTế phầnCàiĐặt: ../CôngCụ/xâyDựngTrìnhBiênDịchC.py"""
import importlib as giáTrịThu
import sys as giáTrịHệThốngĐiềuHành
from pathlib import Path as đườngDẫn
giáTrịHệThốngĐiềuHành.path.insert(0, str(đườngDẫn(__file__).resolve().parents[1] / 'CôngCụ'))
if __name__ == '__main__':
    import runpy as TrìnhKhởiChạyChươngTrình
    TrìnhKhởiChạyChươngTrình.run_module('xâyDựngTrìnhBiênDịchC', run_name='__main__', alter_sys=True)
else:
    phầnCàiĐặt = giáTrịThu.import_module('xâyDựngTrìnhBiênDịchC')
    giáTrịPhépÁnhXạ = {'out': 'dữLiệuKếtQuả', 'builtins': 'thànhPhầnDựngSẵn', 'header': 'giáTrịĐầuMục', 'sdk': 'bộCôngCụPhátTriển', 'build_ccompiler': 'tạoTrìnhBiênDịchC', 'i': 'chỉSốThứBậc', 'elf': 'tệpTệpThựcThi', 'run': 'thựcThiLệnh', 'flags': 'cácBitCấuHình', 'path': 'đườngDẫn', 'p': 'vịTríDữLiệu', 'cc': 'TrìnhBiênDịchC', 'obj': 'tệpĐích', 'flag': 'giáTrịCácThiếtLập', 'ld': 'côngCụTrìnhLiênKết', 'objects': 'cácTệpĐích', 'repo': 'đườngDẫnKhoNguồn', 'v': 'dữLiệuTạm', 'upstream': 'nguồnGốc', 'root': 'địaChỉGốcCây', 'assets': 'tàiNguyênKèm', 'source': 'dữLiệuNguyênBản', 'name': 'tên', 'includes': 'cóBaoGồm'}
    for phầnMụcTrướcĐó, phầnMụcHiệnTại in giáTrịPhépÁnhXạ.items():
        if hasattr(phầnCàiĐặt, phầnMụcHiệnTại): globals()[phầnMụcTrướcĐó] = getattr(phầnCàiĐặt, phầnMụcHiệnTại)
