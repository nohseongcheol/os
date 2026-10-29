#!/usr/bin/env python3
"""기존 đườngDẫn 호환 điểmMục. dữLiệuThựcTế phầnCàiĐặt: ../CôngCụ/cầuNốiMạng.py"""
import importlib as giáTrịThu
import sys as giáTrịHệThốngĐiềuHành
from pathlib import Path as đườngDẫn
giáTrịHệThốngĐiềuHành.path.insert(0, str(đườngDẫn(__file__).resolve().parents[1] / 'CôngCụ'))
if __name__ == '__main__':
    import runpy as TrìnhKhởiChạyChươngTrình
    TrìnhKhởiChạyChươngTrình.run_module('cầuNốiMạng', run_name='__main__', alter_sys=True)
else:
    phầnCàiĐặt = giáTrịThu.import_module('cầuNốiMạng')
    giáTrịPhépÁnhXạ = {'response': 'phảnHồi', 'parts': 'thànhPhầnĐườngDẫn', 's': 'dữLiệuChuỗi', 'i': 'chỉSốThứBậc', 'close': 'đóng', 'forward': 'quyTắcViệcChuyểnTiếp', 'slip_input': 'đầuVàoSLIP', 'self': 'giáTrịBảnThân', 'item': 'giáTrịMục', 'flags': 'cácBitCấuHình', 'ftp_port': 'sốCổngChuyểnGiaoTệp', 'args': 'mảngĐốiSố', 'server': 'giáTrịMáyChủ', 'data': 'DữLiệu', 'ethernet_input': 'đầuVàoEthernet', 'trace_packet': 'góiTinDấuVết', 'GATEWAY': 'địaChỉPhầnCứngCổngNối', 'rule': 'giáTrịQuyTắc', 'protocol': 'ABIMạng', 'forwards': 'cácQuyTắcViệcChuyểnTiếp', 'occupied': 'đãChiếm', 'host': 'Chủ', 'ack': 'sốSựXácNhận', 'serial_port': 'sốCổngNốiTiếp', 'readers': 'cácBộĐọc', 'guest': 'khách', 'destination': 'địaChỉDữLiệuĐích', 'ethernet_port': 'cổngEthernet', 'b': 'giáTrịThứHai', 'MAC': 'địaChỉMáy', 'arp': 'góiTinĐộPhânGiảiĐịaChỉ', 'writable': 'ghiĐược', 'direction': 'hướng', 'seq': 'sốThứTự', 'frame': 'khungViệcThựcThi', 'loop': 'giáTrịChuKỳ', 'port': 'sốCổng', 'offset': 'giáTrịĐộLệch', 'readable': 'cóThểĐọc', 'c': 'mãKýTự', 'p': 'vịTríDữLiệu', 'writers': 'cácBộGhi', 'IP': 'giáTrịĐịaChỉLiênMạng', 'e': 'mụcPhụTrợ', 'n': 'sốLượngPhầnMục', 'packet': 'dữLiệuGóiTin', 'arguments': 'đốiSốĐãChuyểnTiếp', 'source': 'dữLiệuNguyênBản', 'NetworkBridge': 'cầuNốiMạng', 'window': 'cửaSổ', 'capture': 'thuGiữ'}
    for phầnMụcTrướcĐó, phầnMụcHiệnTại in giáTrịPhépÁnhXạ.items():
        if hasattr(phầnCàiĐặt, phầnMụcHiệnTại): globals()[phầnMụcTrướcĐó] = getattr(phầnCàiĐặt, phầnMụcHiệnTại)
