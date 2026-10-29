#!/usr/bin/env python3
"""기존 đườngDẫn 호환 điểmMục. dữLiệuThựcTế phầnCàiĐặt: ../CôngCụ/MáyChủVọngMẫu.py"""
import importlib as giáTrịThu
import sys as giáTrịHệThốngĐiềuHành
from pathlib import Path as đườngDẫn
giáTrịHệThốngĐiềuHành.path.insert(0, str(đườngDẫn(__file__).resolve().parents[1] / 'CôngCụ'))
if __name__ == '__main__':
    import runpy as TrìnhKhởiChạyChươngTrình
    TrìnhKhởiChạyChươngTrình.run_module('MáyChủVọngMẫu', run_name='__main__', alter_sys=True)
else:
    phầnCàiĐặt = giáTrịThu.import_module('MáyChủVọngMẫu')
    giáTrịPhépÁnhXạ = {'data': 'DữLiệu', 'sock': 'giáTrịỔCắmMạng', 'tcp_port': 'cổngTCP', 'chunk': 'giáTrịĐoạn', 'received': 'cóĐãNhận', 'self': 'giáTrịBảnThân', 'UDP': 'yêuCầuThẻXửLýĐiệnDữLiệu', 'thread': 'bộLàmViệc', 'echo': 'mụcMáyChủVọngLại', 'TCP': 'yêuCầuKếtNốiThẻXửLý', 'EchoServers': 'CácMáyChủVọngLại', 'parser': 'bộPhânTích', 'server': 'giáTrịMáyChủ', 'udp_port': 'cổngUDP', 'args': 'mảngĐốiSố'}
    for phầnMụcTrướcĐó, phầnMụcHiệnTại in giáTrịPhépÁnhXạ.items():
        if hasattr(phầnCàiĐặt, phầnMụcHiệnTại): globals()[phầnMụcTrướcĐó] = getattr(phầnCàiĐặt, phầnMụcHiệnTại)
