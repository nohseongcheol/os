#!/usr/bin/env python3
"""기존 đườngDẫn 호환 điểmMục. dữLiệuThựcTế phầnCàiĐặt: ../CôngCụ/xâyDựngPython.py"""
import importlib as giáTrịThu
import sys as giáTrịHệThốngĐiềuHành
from pathlib import Path as đườngDẫn
giáTrịHệThốngĐiềuHành.path.insert(0, str(đườngDẫn(__file__).resolve().parents[1] / 'CôngCụ'))
if __name__ == '__main__':
    import runpy as TrìnhKhởiChạyChươngTrình
    TrìnhKhởiChạyChươngTrình.run_module('xâyDựngPython', run_name='__main__', alter_sys=True)
else:
    phầnCàiĐặt = giáTrịThu.import_module('xâyDựngPython')
    giáTrịPhépÁnhXạ = {'ld': 'côngCụTrìnhLiênKết', 'archive': 'khoLưuTrữ', 'SHA256': 'mãBămViệcThẩmĐịnh', 'build_python': 'tạoPython', 'root': 'địaChỉGốcCây', 'source': 'dữLiệuNguyênBản', 'name': 'tên', 'path': 'đườngDẫn', 'VERSION': 'giáTrịPhiênBảnNgônNgữ', 'cc': 'TrìnhBiênDịchC', 'tar': 'góiGộpTAR', 'newlib': 'newlib', 'member': 'thànhViên'}
    for phầnMụcTrướcĐó, phầnMụcHiệnTại in giáTrịPhépÁnhXạ.items():
        if hasattr(phầnCàiĐặt, phầnMụcHiệnTại): globals()[phầnMụcTrướcĐó] = getattr(phầnCàiĐặt, phầnMụcHiệnTại)
