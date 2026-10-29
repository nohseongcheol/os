#!/usr/bin/env python3
"""기존 đườngDẫn 호환 điểmMục. dữLiệuThựcTế phầnCàiĐặt: ../CôngCụ/thửELF.py"""
import importlib as giáTrịThu
import sys as giáTrịHệThốngĐiềuHành
from pathlib import Path as đườngDẫn
giáTrịHệThốngĐiềuHành.path.insert(0, str(đườngDẫn(__file__).resolve().parents[1] / 'CôngCụ'))
if __name__ == '__main__':
    import runpy as TrìnhKhởiChạyChươngTrình
    TrìnhKhởiChạyChươngTrình.run_module('thửELF', run_name='__main__', alter_sys=True)
else:
    phầnCàiĐặt = giáTrịThu.import_module('thửELF')
    giáTrịPhépÁnhXạ = {'out': 'dữLiệuKếtQuả', 'expected': 'dựKiến', 'phoff': 'độLệchĐầuMụcChươngTrình', 'offset': 'giáTrịĐộLệch', 'invalid': 'dữLiệuKhôngHợpLệ', 'path': 'đườngDẫn', 'executable': 'ảnhTệpThựcThi', 'rejected': 'kếtQuảSựTừChối', 'linux_example': 'víDụLinux', 'original': 'nguyênBản', 'result': 'kếtQuả', 'format_': 'chọnĐịnhDạng', 'main': 'chạy', 'content': 'giáTrịNộiDung', 'source': 'dữLiệuNguyênBản', 'name': 'tên', 'reference': 'mốcCơSởPhépSoSánh', 'ROOT': 'gốcCâyDựÁn', 'value': 'giáTrị', 'report': 'báoCáoViệcThẩmĐịnh'}
    for phầnMụcTrướcĐó, phầnMụcHiệnTại in giáTrịPhépÁnhXạ.items():
        if hasattr(phầnCàiĐặt, phầnMụcHiệnTại): globals()[phầnMụcTrướcĐó] = getattr(phầnCàiĐặt, phầnMụcHiệnTại)
