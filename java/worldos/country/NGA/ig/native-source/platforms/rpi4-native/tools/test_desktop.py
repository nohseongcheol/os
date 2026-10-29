#!/usr/bin/env python3
"""기존 ụzọ_ozi 호환 ndebà_akara. ǹdịnezie_datà 구현: ../Ngwaọrụ/바탕화면시험.py"""
import importlib as 가져오기
import sys as OS_valuu
from pathlib import Path as ụzọ_ozi
OS_valuu.path.insert(0, str(ụzọ_ozi(__file__).resolve().parents[1] / 'Ngwaọrụ'))
if __name__ == '__main__':
    import runpy as app_ihengosi_ndi_app
    app_ihengosi_ndi_app.run_module('바탕화면시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('바탕화면시험')
    대응 = {'x': 'ngakọrịta_x', 'typing': '글자입력', 'message': '알림문', 'start': 'Bido', 'down': '누르는중', 'exact': '정확한값', 'i': '순번', 'press': '글쇠누르기', 'rectangles': '사각형들', 'sym': 'adimara', 'j': '안쪽순번', 'deadline': '마감시각', 'proc': 'ùsòrò', 'data': 'datà', 'main': 'Bido', 'w': '너비값', 'init': '초기값', 'block': 'datà_gbochie', 'ROOT': '기준', 'text': 'SMS', 'marker': '확인표시', 'report': 'nkwèputaonòdù_akụkọ', 'until': '까지', 'clipboard': 'bọọd_ntipanye_valuu', 'dst': 'ebemwèga_àdreèsì', 'seen': '본항목들', 'poll': '준비살피미', 'transcript': '대화기록', 'port': '접속번호', 'offset': 'Nnokwata_valuu', 'h': '높이값', 'src': '원본주소', 'event': 'mmèrème', 'encoding': 'òtù_mkpụrụedemede', 'size': 'Ụhara', 'key': '누름값', 'pixels': '화소들', 'y': '세로좌표', 'output': '출력결과', 'symbol': 'adimara_valuu', 'client': 'klayènt', 'char': 'mkpụrụedemede_datà', 'rgb': '빛삼원색'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
