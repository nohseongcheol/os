#!/usr/bin/env python3
"""기존 đườngDẫn 호환 điểmMục. dữLiệuThựcTế phầnCàiĐặt: ../CôngCụ/thửSwing.py"""
import importlib as giáTrịThu
import sys as giáTrịHệThốngĐiềuHành
from pathlib import Path as đườngDẫn
giáTrịHệThốngĐiềuHành.path.insert(0, str(đườngDẫn(__file__).resolve().parents[1] / 'CôngCụ'))
if __name__ == '__main__':
    import runpy as TrìnhKhởiChạyChươngTrình
    TrìnhKhởiChạyChươngTrình.run_module('thửSwing', run_name='__main__', alter_sys=True)
else:
    phầnCàiĐặt = giáTrịThu.import_module('thửSwing')
    giáTrịPhépÁnhXạ = {'wait': 'đợi', 'x': 'tọaĐộX', 's': 'dữLiệuChuỗi', 'i': 'chỉSốThứBậc', 'sel': 'BộChọn', 'seconds': 'đơnVịGiây', 'log': 'bảnGhiNhậtKý', 'data': 'DữLiệu', 'at': 'vịTríHiệnTại', 'send': 'gửi', 'main': 'chạy', 'req': 'giáTrịYêuCầu', 'hot': 'giáTrịLốiTắt', 'pump': 'sựKiệnThẻXửLý', 'ROOT': 'gốcCâyDựÁn', 'marker': 'dấuMốc', 'b': 'giáTrịThứHai', 'command': 'lệnh', 'shell': 'vỏLệnh', 'f': 'mụcTệp', 'click': 'nútNhấnChuột', 'k': 'chỉSốThứBa', 'c': 'mãKýTự', 'r': 'giáTrịĐãTrảVề', 'p': 'vịTríDữLiệu', 'command_mode': 'chếĐộLệnh', 'end': 'độLệchKếtThúc', 'classes': 'đườngDẫnLớp', 'key': 'giáTrịĐãNhấn', 'y': 'tọaĐộY', 'result': 'kếtQuả', 'report': 'báoCáoViệcThẩmĐịnh', 'dest': 'vịTríGiáTrịĐích', 'work': 'đườngDẫnĐangLàmViệc', 'qmp': 'kếtNốiĐiềuKhiểnGiảLập'}
    for phầnMụcTrướcĐó, phầnMụcHiệnTại in giáTrịPhépÁnhXạ.items():
        if hasattr(phầnCàiĐặt, phầnMụcHiệnTại): globals()[phầnMụcTrướcĐó] = getattr(phầnCàiĐặt, phầnMụcHiệnTại)
