#!/usr/bin/env python3
"""기존 đườngDẫn 호환 điểmMục. dữLiệuThựcTế phầnCàiĐặt: ../CôngCụ/thửFTP.py"""
import importlib as giáTrịThu
import sys as giáTrịHệThốngĐiềuHành
from pathlib import Path as đườngDẫn
giáTrịHệThốngĐiềuHành.path.insert(0, str(đườngDẫn(__file__).resolve().parents[1] / 'CôngCụ'))
if __name__ == '__main__':
    import runpy as TrìnhKhởiChạyChươngTrình
    TrìnhKhởiChạyChươngTrình.run_module('thửFTP', run_name='__main__', alter_sys=True)
else:
    phầnCàiĐặt = giáTrịThu.import_module('thửFTP')
    giáTrịPhépÁnhXạ = {'timeout': 'hếtGiờViệcThựcThi', 'payload': 'dữLiệuNộiTải', 'broken': 'hỏng', 'linux_example': 'víDụLinux', 'chunk': 'giáTrịĐoạn', 'data': 'DữLiệu', 'proc': 'tiếnTrình', 'code': 'dãyChỉLệnh', 'linux': 'tệpLinux', 'archive': 'khoLưuTrữ', 'main': 'chạy', 'net_source': 'nguồnMạngGọn', 'temporary': 'tạm', 'static_source': 'nguồnTĩnh', 'java_source': 'nguồnJava', 'echo': 'mụcMáyChủVọngLại', 'ROOT': 'gốcCâyDựÁn', 'text': 'vănBản', 'marker': 'dấuMốc', 'EchoFixture': 'MẫuThửVọngLại', 'command': 'lệnh', 'out': 'dữLiệuKếtQuả', 'expected': 'dựKiến', 'server_source': 'nguồnMáyChủ', 'shell': 'vỏLệnh', 'upload': 'cácTệpTảiLên', 'transcript': 'bảnGhiDiễnTiến', 'port': 'sốCổng', 'native': 'bảnĐịa', 'elf': 'tệpTệpThựcThi', 'server_udp_port': 'cổngĐiệnDữLiệuMáyChủ', 'packed': 'đãĐóngGói', 'bridge': 'cầuNối', 'selector': 'bộChọn', 'end': 'độLệchKếtThúc', 'e': 'mụcPhụTrợ', 'ftp': 'kếtNốiChuyểnGiaoTệp', 'key': 'giáTrịĐãNhấn', 'bytecode': 'mãByte', 'peer': 'giáTrịĐốiTác', 'result': 'kếtQuả', 'unchanged': 'dữLiệuĐãGiữNguyên', 'line': 'dòng', 'server_tcp_port': 'cổngLuồngMáyChủ', 'source': 'dữLiệuNguyênBản', 'NetworkBridge': 'cầuNốiMạng', 'jar': 'góiGộpJava', 'receive': 'nhậnThôngĐiệp', 'report': 'báoCáoViệcThẩmĐịnh'}
    for phầnMụcTrướcĐó, phầnMụcHiệnTại in giáTrịPhépÁnhXạ.items():
        if hasattr(phầnCàiĐặt, phầnMụcHiệnTại): globals()[phầnMụcTrướcĐó] = getattr(phầnCàiĐặt, phầnMụcHiệnTại)
