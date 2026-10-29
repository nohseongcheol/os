#!/usr/bin/env python3
"""기존 đườngDẫn 호환 điểmMục. dữLiệuThựcTế phầnCàiĐặt: ../CôngCụ/khungNhìnMànLàmViệc.py"""
import importlib as giáTrịThu
import sys as giáTrịHệThốngĐiềuHành
from pathlib import Path as đườngDẫn
giáTrịHệThốngĐiềuHành.path.insert(0, str(đườngDẫn(__file__).resolve().parents[1] / 'CôngCụ'))
if __name__ == '__main__':
    import runpy as TrìnhKhởiChạyChươngTrình
    TrìnhKhởiChạyChươngTrình.run_module('khungNhìnMànLàmViệc', run_name='__main__', alter_sys=True)
else:
    phầnCàiĐặt = giáTrịThu.import_module('khungNhìnMànLàmViệc')
    giáTrịPhépÁnhXạ = {'count': 'sốLượngMục', 'special': 'phímĐặcBiệt', 'error': 'lỗi', 'exact': 'giáTrịChínhXác', 'network': 'mạng', 'closed': 'làĐãĐóng', 'length': 'độDài', 'opened': 'đãMở', 'ftp_port': 'sốCổngChuyểnGiaoTệp', 'server': 'giáTrịMáyChủ', 'resources': 'cácTàiNguyên', 'data': 'DữLiệu', 'shift': 'phímDịch', 'send': 'gửi', 'run_desktop': 'chạyMànLàmViệc', 'protocol': 'ABIMạng', 'forwards': 'cácQuyTắcViệcChuyểnTiếp', 'host': 'Chủ', 'text': 'vănBản', 'korean': 'tiếngHàn', 'port': 'sốCổng', 'signum': 'sốTínHiệu', 'version': 'sốPhiênBản', 'parser': 'bộPhânTích', 'bridge': 'cầuNối', 'kind': 'giáTrịLoạiMục', 'tail': 'phầnPhầnKết', 'size': 'cỡ', 'previous_buttons': 'cácNútTrướcĐó', 'key': 'giáTrịĐãNhấn', 'y': 'tọaĐộY', 'prefix': 'phầnDẫnĐầu', 'client': 'máyKhách', 'char': 'dữLiệuKýTự', 'work': 'đườngDẫnĐangLàmViệc', 'Keyboard': 'BànPhím', 'x': 'tọaĐộX', 'down': 'làĐangNhấn', 'net': 'mụcCầuNốiMạng', 'self': 'giáTrịBảnThân', 'mode_changed': 'đãĐổiChếĐộ', 'serial': 'vàoRaNốiTiếp', 'args': 'mảngĐốiSố', 'Hangul': 'ghépHangul', 'chunk': 'giáTrịĐoạn', 'proc': 'tiếnTrình', 'Desktop': 'kếtNốiMànLàmViệc', 'buttons': 'cácNút', 'thread': 'bộLàmViệc', 'pressed': 'làĐãNhấn', 'previous': 'trướcĐó', 'toggle': 'chếĐộChuyển', 'command': 'lệnh', 'sock': 'giáTrịỔCắmMạng', 'frame': 'khungViệcThựcThi', 'ctrl': 'phímĐiềuKhiển', 'path': 'đườngDẫn', 'cp': 'mãHóaKýTự', 'terminate': 'chấmDứt', 'security': 'bảoMật', 'vnc_port': 'cổngVNC', 'body': 'vănBảnThân', 'index': 'chỉSốTraCứu', 'exited': 'cóĐãRa', 'keysym': 'kýHiệuPhím', 'output': 'đầuRa', 'keyboard': 'mụcBànPhím', 'interrupted': 'đãBịNgắt', 'listener': 'nhậnCổng', 'reader': 'bộĐọc', 'NetworkBridge': 'cầuNốiMạng', 'gui': 'mànHìnhBảnVẽ', 'worker': 'tácVụViệcXửLý'}
    for phầnMụcTrướcĐó, phầnMụcHiệnTại in giáTrịPhépÁnhXạ.items():
        if hasattr(phầnCàiĐặt, phầnMụcHiệnTại): globals()[phầnMụcTrướcĐó] = getattr(phầnCàiĐặt, phầnMụcHiệnTại)
