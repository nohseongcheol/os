#!/usr/bin/env python3
"""기존 tsela 호환 tsenyo_ntlha. tota_tshedimosetso 구현: ../Thuluse/바탕화면시험.py"""
import importlib as 가져오기
import sys as Tsamaisotiriso_Boleng
from pathlib import Path as tsela
Tsamaisotiriso_Boleng.path.insert(0, str(tsela(__file__).resolve().parents[1] / 'Thuluse'))
if __name__ == '__main__':
    import runpy as Tiriso_llae_ya_sediriso
    Tiriso_llae_ya_sediriso.run_module('바탕화면시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('바탕화면시험')
    대응 = {'x': 'kgokagano_ya_x', 'typing': '글자입력', 'message': '알림문', 'start': 'dirisa', 'down': '누르는중', 'exact': '정확한값', 'i': '순번', 'press': '글쇠누르기', 'rectangles': '사각형들', 'sym': 'letshwao', 'j': '안쪽순번', 'deadline': '마감시각', 'proc': 'Thulaganyo', 'data': 'tshedimosetso', 'main': 'dirisa', 'w': '너비값', 'init': '초기값', 'block': 'tshedimosetso_thibela', 'ROOT': '기준', 'text': 'SMS', 'marker': '확인표시', 'report': 'netefatso_pego', 'until': '까지', 'clipboard': 'peelodimamaretswa_Boleng', 'dst': 'bogorogelo_aterese', 'seen': '본항목들', 'poll': '준비살피미', 'transcript': '대화기록', 'port': '접속번호', 'offset': 'Baya_ka_Tekatekanyo_Boleng', 'h': '높이값', 'src': '원본주소', 'event': 'tiragalo', 'encoding': 'Setlhophatshwao', 'size': 'lekanya', 'key': '누름값', 'pixels': '화소들', 'y': '세로좌표', 'output': '출력결과', 'symbol': 'letshwao_Boleng', 'client': 'sedirelwa', 'char': 'Letshwao_tshedimosetso', 'rgb': '빛삼원색'}
    for 이전, ga_jaana_selwana in 대응.items():
        if hasattr(구현, ga_jaana_selwana): globals()[이전] = getattr(구현, ga_jaana_selwana)
