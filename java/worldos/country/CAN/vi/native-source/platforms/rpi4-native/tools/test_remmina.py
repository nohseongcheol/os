#!/usr/bin/env python3
"""기존 đườngDẫn 호환 điểmMục. dữLiệuThựcTế phầnCàiĐặt: ../CôngCụ/thửRemmina.py"""
import importlib as giáTrịThu
import sys as giáTrịHệThốngĐiềuHành
from pathlib import Path as đườngDẫn
giáTrịHệThốngĐiềuHành.path.insert(0, str(đườngDẫn(__file__).resolve().parents[1] / 'CôngCụ'))
if __name__ == '__main__':
    import runpy as TrìnhKhởiChạyChươngTrình
    TrìnhKhởiChạyChươngTrình.run_module('thửRemmina', run_name='__main__', alter_sys=True)
else:
    phầnCàiĐặt = giáTrịThu.import_module('thửRemmina')
    giáTrịPhépÁnhXạ = {'wait': 'đợi', 'typing': 'kýTựCóKiểu', 'start': 'chạy', 'profile': 'hồSơ', 'focused': 'cóTiêuĐiểm', 'serial': 'vàoRaNốiTiếp', 'keys': 'cácPhímĐãNhấn', 'server': 'giáTrịMáyChủ', 'log': 'bảnGhiNhậtKý', 'args': 'mảngĐốiSố', 'deadline': 'thờiGianHạnChót', 'data': 'DữLiệu', 'candidate': 'ứngViên', 'logs': 'cácBảnGhiNhậtKý', 'kw': 'đốiSốĐượcĐặtTên', 'number': 'giáTrịThuộcSố', 'main': 'chạy', 'ready': 'đầyĐủSựChuẩnBị', 'found': 'tìmKiếmKếtQuả', 'guest': 'khách', 'ROOT': 'gốcCâyDựÁn', 'marker': 'dấuMốc', 'text': 'vănBản', 'out': 'dữLiệuKếtQuả', 'env': 'môiTrường', 'f': 'mụcTệp', 'port': 'sốCổng', 'offset': 'giáTrịĐộLệch', 'version': 'sốPhiênBản', 'p': 'vịTríDữLiệu', 'selector': 'bộChọn', 'xvfb': 'hiểnThịẢo', 'display': 'thiếtBịHiểnThị', 'n': 'sốLượngPhầnMục', 'key': 'giáTrịĐãNhấn', 'processes': 'cácTiếnTrìnhĐangChạy', 'rootfs': 'hệTệpGốc', 'xdo': 'côngCụĐầuVàoẢo', 'name': 'tên', 'window': 'cửaSổ', 'report': 'báoCáoViệcThẩmĐịnh', 'work': 'đườngDẫnĐangLàmViệc'}
    for phầnMụcTrướcĐó, phầnMụcHiệnTại in giáTrịPhépÁnhXạ.items():
        if hasattr(phầnCàiĐặt, phầnMụcHiệnTại): globals()[phầnMụcTrướcĐó] = getattr(phầnCàiĐặt, phầnMụcHiệnTại)
