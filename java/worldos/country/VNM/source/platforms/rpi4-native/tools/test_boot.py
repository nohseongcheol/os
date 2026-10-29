#!/usr/bin/env python3
"""기존 đườngDẫn 호환 điểmMục. dữLiệuThựcTế phầnCàiĐặt: ../CôngCụ/ThửKhởiĐộng.py"""
import importlib as giáTrịThu
import sys as giáTrịHệThốngĐiềuHành
from pathlib import Path as đườngDẫn
giáTrịHệThốngĐiềuHành.path.insert(0, str(đườngDẫn(__file__).resolve().parents[1] / 'CôngCụ'))
if __name__ == '__main__':
    import runpy as TrìnhKhởiChạyChươngTrình
    TrìnhKhởiChạyChươngTrình.run_module('ThửKhởiĐộng', run_name='__main__', alter_sys=True)
else:
    phầnCàiĐặt = giáTrịThu.import_module('ThửKhởiĐộng')
    giáTrịPhépÁnhXạ = {'timeout': 'hếtGiờViệcThựcThi', 'response': 'phảnHồi', 'msg': 'thôngĐiệpMạng', 'exact': 'giáTrịChínhXác', 'markers': 'cácDấuMốc', 'i': 'chỉSốThứBậc', 'match': 'làBằng', 'execute': 'thựcThiTácVụ', 'cancel': 'thaoTácHủy', 'cmd_byte': 'byteLệnh', 'reply': 'lờiĐáp', 'points': 'cácĐiểm', 'server': 'giáTrịMáyChủ', 'data': 'DữLiệu', 'prompt': 'dấuNhắc', 'enter': 'vào', 'imported': 'đãNhập', 'send': 'gửi', 'main': 'chạy', 'ROOT': 'gốcCâyDựÁn', 'text': 'vănBản', 'first_gui': 'giaoDiệnĐồHọaĐầuTiên', 'pixel': 'điểmẢnh', 'java_class': 'lớpJava', 'upload': 'cácTệpTảiLên', 'pixels_file': 'tệpĐiểmẢnh', 'pixels_data': 'dữLiệuĐiểmẢnh', 'edit': 'giáTrịSửa', 'receive_until': 'nhậnĐếnKhi', 'selector': 'bộChọn', 'size': 'cỡ', 'qmp_path': 'đườngDẫnQMP', 'key': 'giáTrịĐãNhấn', 'second_gui': 'giaoDiệnĐồHọaThứHai', 'y': 'tọaĐộY', 'result': 'kếtQuả', 'samples': 'cácMụcVíDụ', 'client': 'máyKhách', 'line': 'dòng', 'report': 'báoCáoViệcThẩmĐịnh', 'work': 'đườngDẫnĐangLàmViệc', 'x': 'tọaĐộX', 'python_checks': 'cácPhépKiểmTraPython', 'download': 'tảiXuống', 'greeting': 'LờiChào', 'dims': 'giáTrịCácChiều', 'chunk': 'giáTrịĐoạn', 'deadline': 'thờiGianHạnChót', 'proc': 'tiếnTrình', 'content': 'giáTrịNộiDung', 'block': 'khốiDữLiệu', 'marker': 'dấuMốc', 'command': 'lệnh', 'expected': 'dựKiến', 'shell': 'vỏLệnh', 'drawing': 'đườngDẫnBảnVẽ', 'f': 'mụcTệp', 'transcript': 'bảnGhiDiễnTiến', 'offset': 'giáTrịĐộLệch', 'path': 'đườngDẫn', 'screenshot': 'ảnhMànHình', 'arguments': 'đốiSốĐãChuyểnTiếp', 'pixels': 'danhSáchCácĐiểmẢnh', 'viewer': 'máyKháchMànHình', 'output': 'đầuRa', 'stream': 'giáTrịLuồng', 'cmd': 'cácĐốiSốLệnh', 'name': 'tên', 'qmp': 'kếtNốiĐiềuKhiểnGiảLập'}
    for phầnMụcTrướcĐó, phầnMụcHiệnTại in giáTrịPhépÁnhXạ.items():
        if hasattr(phầnCàiĐặt, phầnMụcHiệnTại): globals()[phầnMụcTrướcĐó] = getattr(phầnCàiĐặt, phầnMụcHiệnTại)
