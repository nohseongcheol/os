#!/usr/bin/env python3
"""기존 yo_l 호환 kiritish_nuqta. real_ma_lumotlar 구현: ../Vositalar/바탕화면시험.py"""
import importlib as TAKE_VALUE
import sys as operatsion_tizim_VALUE
from pathlib import Path as yo_l
operatsion_tizim_VALUE.path.insert(0, str(yo_l(__file__).resolve().parents[1] / 'Vositalar'))
if __name__ == '__main__':
    import runpy as ilova_ilovalar_paneli
    ilova_ilovalar_paneli.run_module('바탕화면시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('바탕화면시험')
    대응 = {'x': 'x_koordinata', 'typing': '글자입력', 'message': '알림문', 'start': 'Bajarish', 'down': '누르는중', 'exact': 'EXACT_VALUE', 'i': '순번', 'press': '글쇠누르기', 'rectangles': '사각형들', 'sym': 'ramz', 'j': '안쪽순번', 'deadline': '마감시각', 'proc': 'Jarayon', 'data': 'ma_lumotlar', 'main': 'Bajarish', 'w': '너비값', 'init': '초기값', 'block': 'ma_lumotlar_bloklash', 'ROOT': 'Project_ildiz', 'text': 'Matn', 'marker': '확인표시', 'report': 'tasdiq_hisobot', 'until': '까지', 'clipboard': 'almashish_buferi_VALUE', 'dst': 'ko_chirish_joyi_manzil', 'seen': '본항목들', 'poll': '준비살피미', 'transcript': '대화기록', 'port': '접속번호', 'offset': 'OFFSET_VALUE', 'h': '높이값', 'src': '원본주소', 'event': 'hodisa', 'encoding': 'belgilar_to_plami', 'size': 'Hajmi', 'key': '누름값', 'pixels': '화소들', 'y': 'Y_tugmasi_koordinat', 'output': '출력결과', 'symbol': 'ramz_VALUE', 'client': 'mijoz', 'char': 'belgi_ma_lumotlar', 'rgb': '빛삼원색'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
