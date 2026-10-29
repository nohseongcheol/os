#!/usr/bin/env python3
"""기존 Tsejana 호환 go_tsenya_tshedimošo_ntlha. kgonthe_data 구현: ../Ditholosi/바탕화면시험.py"""
import importlib as 가져오기
import sys as tshepedišotirišo_boleng
from pathlib import Path as Tsejana
tshepedišotirišo_boleng.path.insert(0, str(Tsejana(__file__).resolve().parents[1] / 'Ditholosi'))
if __name__ == '__main__':
    import runpy as tirišo_sethala_tirišo
    tirišo_sethala_tirišo.run_module('바탕화면시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('바탕화면시험')
    대응 = {'x': 'kamano_ya_x', 'typing': '글자입력', 'message': '알림문', 'start': 'Diriša', 'down': '누르는중', 'exact': '정확한값', 'i': '순번', 'press': '글쇠누르기', 'rectangles': '사각형들', 'sym': 'leswao', 'j': '안쪽순번', 'deadline': '마감시각', 'proc': 'tiragalo_a7054519', 'data': 'data', 'main': 'Diriša', 'w': '너비값', 'init': '초기값', 'block': 'data_thibela', 'ROOT': '기준', 'text': 'Sengwalwa', 'marker': '확인표시', 'report': 'tiišetšo_pego', 'until': '까지', 'clipboard': 'klipbote_boleng', 'dst': 'boyo_atrese', 'seen': '본항목들', 'poll': '준비살피미', 'transcript': '대화기록', 'port': '접속번호', 'offset': 'E_Šetšego_boleng', 'h': '높이값', 'src': '원본주소', 'event': 'tiragalo', 'encoding': 'sete_ya_ditlhaka', 'size': 'Bogolo', 'key': '누름값', 'pixels': '화소들', 'y': '세로좌표', 'output': '출력결과', 'symbol': 'leswao_boleng', 'client': 'klaente', 'char': 'tlhaka_data', 'rgb': '빛삼원색'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
