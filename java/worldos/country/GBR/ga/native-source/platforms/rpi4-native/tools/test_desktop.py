#!/usr/bin/env python3
"""기존 CONAIR 호환 iontráil_pointe. iarbhír_sonraí 구현: ../Uirlisí/바탕화면시험.py"""
import importlib as TAKE_VALUE
import sys as córas_oibriúcháin_VALUE
from pathlib import Path as CONAIR
córas_oibriúcháin_VALUE.path.insert(0, str(CONAIR(__file__).resolve().parents[1] / 'Uirlisí'))
if __name__ == '__main__':
    import runpy as clár_tarraiceán_feidhmchlár
    clár_tarraiceán_feidhmchlár.run_module('바탕화면시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('바탕화면시험')
    대응 = {'x': 'x_chomhordanáid', 'typing': '글자입력', 'message': '알림문', 'start': 'Rith_2', 'down': '누르는중', 'exact': 'EXACT_VALUE', 'i': '순번', 'press': '글쇠누르기', 'rectangles': '사각형들', 'sym': 'siombail', 'j': '안쪽순번', 'deadline': '마감시각', 'proc': 'Próiseas', 'data': 'sonraí', 'main': 'Rith_2', 'w': '너비값', 'init': '초기값', 'block': 'sonraí_bac', 'ROOT': 'teilgean_fréamh', 'text': 'Téacs', 'marker': '확인표시', 'report': 'bailíochtú_tuairisc', 'until': '까지', 'clipboard': 'gearrthaisce_VALUE', 'dst': 'sprioc_ADDRESS_08bbd577', 'seen': '본항목들', 'poll': '준비살피미', 'transcript': '대화기록', 'port': 'uimhir_phoirt', 'offset': 'OFFSET_VALUE', 'h': '높이값', 'src': '원본주소', 'event': 'ócáid', 'encoding': 'tacar_carachtar', 'size': 'Méid', 'key': '누름값', 'pixels': '화소들', 'y': '세로좌표', 'output': '출력결과', 'symbol': 'siombail_VALUE', 'client': 'cliant', 'char': 'carachtar_sonraí', 'rgb': '빛삼원색'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
