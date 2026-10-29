#!/usr/bin/env python3
"""기존 đườngDẫn 호환 điểmMục. dữLiệuThựcTế phầnCàiĐặt: ../CôngCụ/thựcThiLệnh.py"""
import importlib as giáTrịThu
import sys as giáTrịHệThốngĐiềuHành
from pathlib import Path as đườngDẫn
giáTrịHệThốngĐiềuHành.path.insert(0, str(đườngDẫn(__file__).resolve().parents[1] / 'CôngCụ'))
if __name__ == '__main__':
    import runpy as TrìnhKhởiChạyChươngTrình
    TrìnhKhởiChạyChươngTrình.run_module('thựcThiLệnh', run_name='__main__', alter_sys=True)
else:
    phầnCàiĐặt = giáTrịThu.import_module('thựcThiLệnh')
    giáTrịPhépÁnhXạ = {'supported': 'cácTínhNăngĐượcHỗTrợ', 'parser': 'bộPhânTích', 'qemu': 'MáyGiảLập', 'run_desktop': 'chạyMànLàmViệc', 'main': 'chạy', 'host': 'Chủ', 'status': 'giáTrịTrạngThái', 'NetworkBridge': 'cầuNốiMạng', 'ROOT': 'gốcCâyDựÁn', 'bridge': 'cầuNối', 'loader': 'bộNạp', 'base': 'giáTrịNền', 'options': 'cácTùyChọn', 'binary': 'nhịPhân', 'args': 'mảngĐốiSố', 'command': 'lệnh'}
    for phầnMụcTrướcĐó, phầnMụcHiệnTại in giáTrịPhépÁnhXạ.items():
        if hasattr(phầnCàiĐặt, phầnMụcHiệnTại): globals()[phầnMụcTrướcĐó] = getattr(phầnCàiĐặt, phầnMụcHiệnTại)
