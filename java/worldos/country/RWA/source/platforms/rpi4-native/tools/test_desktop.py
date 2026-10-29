#!/usr/bin/env python3
"""기존 Inzira 호환 icyinjizwa_inota. nyakuri_amakurushingiro 구현: ../Ibikoresho/바탕화면시험.py"""
import importlib as 가져오기
import sys as sisitemu_ngengamikorere_agaciro
from pathlib import Path as Inzira
sisitemu_ngengamikorere_agaciro.path.insert(0, str(Inzira(__file__).resolve().parents[1] / 'Ibikoresho'))
if __name__ == '__main__':
    import runpy as porogaramu_umukozi
    porogaramu_umukozi.run_module('바탕화면시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('바탕화면시험')
    대응 = {'x': 'Ihuza_rya_x', 'typing': '글자입력', 'message': '알림문', 'start': 'ihuriro', 'down': '누르는중', 'exact': '정확한값', 'i': '순번', 'press': '글쇠누르기', 'rectangles': '사각형들', 'sym': 'ikimenyetso', 'j': '안쪽순번', 'deadline': '마감시각', 'proc': 'Inzira_a7054519', 'data': 'amakurushingiro', 'main': 'ihuriro', 'w': '너비값', 'init': '초기값', 'block': 'amakurushingiro_guheza', 'ROOT': '기준', 'text': 'Umwandiko', 'marker': '확인표시', 'report': 'iyemeza_raporo', 'until': '까지', 'clipboard': 'ububikogateganyo_agaciro', 'dst': 'aho_ijya_aderesi', 'seen': '본항목들', 'poll': '준비살피미', 'transcript': '대화기록', 'port': '접속번호', 'offset': 'Ofuseti_agaciro', 'h': '높이값', 'src': '원본주소', 'event': 'icyabaye', 'encoding': 'itsinda_ry_inyuguti', 'size': 'Ingano', 'key': '누름값', 'pixels': '화소들', 'y': '세로좌표', 'output': '출력결과', 'symbol': 'ikimenyetso_agaciro', 'client': 'umukiriya', 'char': 'inyuguti_amakurushingiro', 'rgb': '빛삼원색'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
