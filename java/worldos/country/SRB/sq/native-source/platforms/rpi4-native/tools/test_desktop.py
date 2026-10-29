#!/usr/bin/env python3
"""기존 POZICIONI 호환 futje_p. aktual_të_dhëna 구현: ../Mjete/바탕화면시험.py"""
import importlib as TAKE_VALUE
import sys as sistem_operativ_VALUE
from pathlib import Path as POZICIONI
sistem_operativ_VALUE.path.insert(0, str(POZICIONI(__file__).resolve().parents[1] / 'Mjete'))
if __name__ == '__main__':
    import runpy as program_hapës
    program_hapës.run_module('바탕화면시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('바탕화면시험')
    대응 = {'x': 'koordinata_x', 'typing': '글자입력', 'message': '알림문', 'start': 'Ekzekuto', 'down': '누르는중', 'exact': 'EXACT_VALUE', 'i': '순번', 'press': 'shtyp_tast', 'rectangles': '사각형들', 'sym': 'simbol', 'j': '안쪽순번', 'deadline': '마감시각', 'proc': 'Proçes', 'data': 'të_dhëna', 'main': 'Ekzekuto', 'w': '너비값', 'init': '초기값', 'block': 'të_dhëna_bllokoj', 'ROOT': 'Project_rrënjë', 'text': 'Teksti', 'marker': '확인표시', 'report': 'miratim_raport', 'until': '까지', 'clipboard': 'kujtesa_e_fragmenteve_VALUE', 'dst': 'vendmbërritje_email', 'seen': '본항목들', 'poll': '준비살피미', 'transcript': '대화기록', 'port': 'numri_i_portës', 'offset': 'OFFSET_VALUE', 'h': '높이값', 'src': '원본주소', 'event': 'Ngjarje', 'encoding': 'bashkësia_e_karaktereve', 'size': 'Madhësi', 'key': '누름값', 'pixels': '화소들', 'y': 'Y_koordinatë', 'output': '출력결과', 'symbol': 'simbol_VALUE', 'client': 'klient', 'char': 'karakter_të_dhëna', 'rgb': '빛삼원색'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
