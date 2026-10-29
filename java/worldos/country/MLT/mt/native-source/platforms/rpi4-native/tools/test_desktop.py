#!/usr/bin/env python3
"""기존 mogħdija 호환 entrata_punt. attwali_data 구현: ../Għodod/바탕화면시험.py"""
import importlib as TAKE_VALUE
import sys as sistema_operattiva_VALUE
from pathlib import Path as mogħdija
sistema_operattiva_VALUE.path.insert(0, str(mogħdija(__file__).resolve().parents[1] / 'Għodod'))
if __name__ == '__main__':
    import runpy as programm_ġabra_ta_apps
    programm_ġabra_ta_apps.run_module('바탕화면시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('바탕화면시험')
    대응 = {'x': 'koordinat_x', 'typing': '글자입력', 'message': '알림문', 'start': 'serje', 'down': '누르는중', 'exact': 'EXACT_VALUE', 'i': '순번', 'press': '글쇠누르기', 'rectangles': '사각형들', 'sym': 'simbolu', 'j': '안쪽순번', 'deadline': '마감시각', 'proc': 'Proċess', 'data': 'data', 'main': 'serje', 'w': '너비값', 'init': '초기값', 'block': 'data_imblokka', 'ROOT': 'pprojetta_għerq', 'text': 'SMS', 'marker': '확인표시', 'report': 'validazzjoni_rapport', 'until': '까지', 'clipboard': 'klibbord_VALUE', 'dst': 'destinazzjoni_ADDRESS', 'seen': '본항목들', 'poll': '준비살피미', 'transcript': '대화기록', 'port': '접속번호', 'offset': 'OFFSET_VALUE', 'h': '높이값', 'src': '원본주소', 'event': 'avveniment', 'encoding': 'sett_ta_karattri', 'size': 'daqqas', 'key': '누름값', 'pixels': '화소들', 'y': '세로좌표', 'output': '출력결과', 'symbol': 'simbolu_VALUE', 'client': 'klijent', 'char': 'karattru_data', 'rgb': '빛삼원색'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
