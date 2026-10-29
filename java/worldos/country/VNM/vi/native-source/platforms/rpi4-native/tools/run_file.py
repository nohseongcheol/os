#!/usr/bin/env python3
"""기존 đườngDẫn 호환 điểmMục. dữLiệuThựcTế phầnCàiĐặt: ../CôngCụ/thựcThiTệp.py"""
import importlib as giáTrịThu
import sys as giáTrịHệThốngĐiềuHành
from pathlib import Path as đườngDẫn
giáTrịHệThốngĐiềuHành.path.insert(0, str(đườngDẫn(__file__).resolve().parents[1] / 'CôngCụ'))
if __name__ == '__main__':
    import runpy as TrìnhKhởiChạyChươngTrình
    TrìnhKhởiChạyChươngTrình.run_module('thựcThiTệp', run_name='__main__', alter_sys=True)
else:
    phầnCàiĐặt = giáTrịThu.import_module('thựcThiTệp')
    giáTrịPhépÁnhXạ = {'timeout': 'hếtGiờViệcThựcThi', 's': 'dữLiệuChuỗi', 'i': 'chỉSốThứBậc', 'match': 'làBằng', 'files': 'danhSáchTệp', 'program': 'chươngTrình', 'executable': 'ảnhTệpThựcThi', 'args': 'mảngĐốiSố', 'chunk': 'giáTrịĐoạn', 'data': 'DữLiệu', 'proc': 'tiếnTrình', 'send': 'gửi', 'main': 'chạy', 'marker': 'dấuMốc', 'command': 'lệnh', 'include': 'baoGồm', 'dumped': 'đãKếtXuất', 'run': 'thựcThiLệnh', 'p': 'vịTríDữLiệu', 'parser': 'bộPhânTích', 'options': 'cácTùyChọn', 'kind': 'giáTrịLoạiMục', 'selector': 'bộChọn', 'upload_data': 'dữLiệuTảiLên', 'end': 'độLệchKếtThúc', 'n': 'sốLượngPhầnMục', 'd': 'dữLiệuĐích', 'key': 'giáTrịĐãNhấn', 'output': 'đầuRa', 'line': 'dòng', 'name': 'tên', 'upload_name': 'tênTảiLên', 'receive': 'nhậnThôngĐiệp'}
    for phầnMụcTrướcĐó, phầnMụcHiệnTại in giáTrịPhépÁnhXạ.items():
        if hasattr(phầnCàiĐặt, phầnMụcHiệnTại): globals()[phầnMụcTrướcĐó] = getattr(phầnCàiĐặt, phầnMụcHiệnTại)
