#!/usr/bin/env python3
"""기존 STIGE 호환 oppføring_p. faktisk_data 구현: ../Verktøy/바탕화면시험.py"""
import importlib as TAKE_VALUE
import sys as operativsystem_VALUE
from pathlib import Path as STIGE
operativsystem_VALUE.path.insert(0, str(STIGE(__file__).resolve().parents[1] / 'Verktøy'))
if __name__ == '__main__':
    import runpy as app_appskuff
    app_appskuff.run_module('바탕화면시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('바탕화면시험')
    대응 = {'x': 'x_koordinat', 'typing': '글자입력', 'message': '알림문', 'start': 'Køyr_2', 'down': '누르는중', 'exact': 'EXACT_VALUE', 'i': '순번', 'press': 'trykkje_tast', 'rectangles': '사각형들', 'sym': 'symbol', 'j': '안쪽순번', 'deadline': '마감시각', 'proc': 'Prosess', 'data': 'data', 'main': 'Køyr_2', 'w': '너비값', 'init': '초기값', 'block': 'data_Blokker', 'ROOT': 'spegle_rot', 'text': 'Tekst', 'marker': '확인표시', 'report': 'validering_rapport', 'until': '까지', 'clipboard': 'utklippstavle_VALUE', 'dst': 'mål_ADDRESS_08bbd577', 'seen': '본항목들', 'poll': '준비살피미', 'transcript': '대화기록', 'port': 'portnummer', 'offset': 'OFFSET_VALUE', 'h': '높이값', 'src': '원본주소', 'event': 'Hending', 'encoding': 'teiknsett', 'size': 'Storleik', 'key': '누름값', 'pixels': '화소들', 'y': 'Y_koordinat', 'output': '출력결과', 'symbol': 'symbol_VALUE', 'client': 'klient', 'char': 'teikn_data', 'rgb': '빛삼원색'}
    for 이전, betalt_vare in 대응.items():
        if hasattr(구현, betalt_vare): globals()[이전] = getattr(구현, betalt_vare)
