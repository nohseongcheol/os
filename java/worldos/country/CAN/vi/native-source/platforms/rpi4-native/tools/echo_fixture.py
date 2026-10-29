#!/usr/bin/env python3
"""기존 đườngDẫn 호환 điểmMục. dữLiệuThựcTế phầnCàiĐặt: ../CôngCụ/MẫuThửVọngLại.py"""
import importlib as giáTrịThu
import sys as giáTrịHệThốngĐiềuHành
from pathlib import Path as đườngDẫn
giáTrịHệThốngĐiềuHành.path.insert(0, str(đườngDẫn(__file__).resolve().parents[1] / 'CôngCụ'))
if __name__ == '__main__':
    import runpy as TrìnhKhởiChạyChươngTrình
    TrìnhKhởiChạyChươngTrình.run_module('MẫuThửVọngLại', run_name='__main__', alter_sys=True)
else:
    phầnCàiĐặt = giáTrịThu.import_module('MẫuThửVọngLại')
    giáTrịPhépÁnhXạ = {'data': 'DữLiệu', 'e': 'mụcPhụTrợ', 'connection': 'kếtNối', 'f': 'mụcTệp', 'peer': 'giáTrịĐốiTác', 'self': 'giáTrịBảnThân', 'udp': 'điềuKhiểnĐiệnDữLiệu', 't': 'mụcThiếtBịCuối', 'tcp': 'điềuKhiểnKếtNối', 'EchoFixture': 'MẫuThửVọngLại', 'args': 'mảngĐốiSố', 'chunk': 'giáTrịĐoạn'}
    for phầnMụcTrướcĐó, phầnMụcHiệnTại in giáTrịPhépÁnhXạ.items():
        if hasattr(phầnCàiĐặt, phầnMụcHiệnTại): globals()[phầnMụcTrướcĐó] = getattr(phầnCàiĐặt, phầnMụcHiệnTại)
