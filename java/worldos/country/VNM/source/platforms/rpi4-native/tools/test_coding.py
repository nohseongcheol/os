#!/usr/bin/env python3
"""기존 đườngDẫn 호환 điểmMục. dữLiệuThựcTế phầnCàiĐặt: ../CôngCụ/thửLậpTrình.py"""
import importlib as giáTrịThu
import sys as giáTrịHệThốngĐiềuHành
from pathlib import Path as đườngDẫn
giáTrịHệThốngĐiềuHành.path.insert(0, str(đườngDẫn(__file__).resolve().parents[1] / 'CôngCụ'))
if __name__ == '__main__':
    import runpy as TrìnhKhởiChạyChươngTrình
    TrìnhKhởiChạyChươngTrình.run_module('thửLậpTrình', run_name='__main__', alter_sys=True)
else:
    phầnCàiĐặt = giáTrịThu.import_module('thửLậpTrình')
    giáTrịPhépÁnhXạ = {'out': 'dữLiệuKếtQuả', 'expected': 'dựKiến', 'sdk': 'bộCôngCụPhátTriển', 'suffix': 'giáTrịHậuTố', 'arc': 'góiGộpĐãNén', 'main': 'chạy', 'elf': 'tệpTệpThựcThi', 'run': 'thựcThiLệnh', 'name': 'tên', 'path': 'đườngDẫn', 'p': 'vịTríDữLiệu', 'ROOT': 'gốcCâyDựÁn', 'report': 'báoCáoViệcThẩmĐịnh', 'args': 'mảngĐốiSố'}
    for phầnMụcTrướcĐó, phầnMụcHiệnTại in giáTrịPhépÁnhXạ.items():
        if hasattr(phầnCàiĐặt, phầnMụcHiệnTại): globals()[phầnMụcTrướcĐó] = getattr(phầnCàiĐặt, phầnMụcHiệnTại)
