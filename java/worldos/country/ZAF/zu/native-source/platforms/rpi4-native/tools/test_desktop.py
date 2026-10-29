#!/usr/bin/env python3
"""기존 Indlela_2 호환 okufakwayo_iphoyinti. ulwazi_ngokwenzekile_imininingwane 구현: ../Amathuluzi/바탕화면시험.py"""
import importlib as 가져오기
import sys as isistimu_yokusebenza_inani
from pathlib import Path as Indlela_2
isistimu_yokusebenza_inani.path.insert(0, str(Indlela_2(__file__).resolve().parents[1] / 'Amathuluzi'))
if __name__ == '__main__':
    import runpy as i_app_ikhabethe_le_app
    i_app_ikhabethe_le_app.run_module('바탕화면시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('바탕화면시험')
    대응 = {'x': 'okuxhumanisa_u_x', 'typing': '글자입력', 'message': '알림문', 'start': 'Sebenzisa', 'down': '누르는중', 'exact': '정확한값', 'i': '순번', 'press': '글쇠누르기', 'rectangles': '사각형들', 'sym': 'uphawu_ad6f1a96', 'j': '안쪽순번', 'deadline': '마감시각', 'proc': 'Inqubo', 'data': 'imininingwane', 'main': 'Sebenzisa', 'w': '너비값', 'init': '초기값', 'block': 'imininingwane_vimbela', 'ROOT': '기준', 'text': 'Itekisi', 'marker': '확인표시', 'report': 'ukufakazisa_umbiko', 'until': '까지', 'clipboard': 'ibhodi_yokunamathisela_inani', 'dst': 'isikhumulo_ikheli', 'seen': '본항목들', 'poll': '준비살피미', 'transcript': '대화기록', 'port': '접속번호', 'offset': 'I_ofisethi_inani', 'h': '높이값', 'src': '원본주소', 'event': 'isigameko', 'encoding': 'iqoqo_lezinhlamvusimo', 'size': 'Ubungako', 'key': '누름값', 'pixels': '화소들', 'y': '세로좌표', 'output': '출력결과', 'symbol': 'uphawu_inani', 'client': 'iklayenti', 'char': 'uhlamvusimo_imininingwane', 'rgb': '빛삼원색'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
