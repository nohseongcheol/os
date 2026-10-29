#!/usr/bin/env python3
"""기존 Ýol 호환 girizmeklik_utuk. hakyky_maglumat 구현: ../Gurallar/바탕화면시험.py"""
import importlib as 가져오기
import sys as operasiýa_ulgamy_baha
from pathlib import Path as Ýol
operasiýa_ulgamy_baha.path.insert(0, str(Ýol(__file__).resolve().parents[1] / 'Gurallar'))
if __name__ == '__main__':
    import runpy as programma_programma_paneli
    programma_programma_paneli.run_module('바탕화면시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('바탕화면시험')
    대응 = {'x': 'x_koordinatasy', 'typing': '글자입력', 'message': '알림문', 'start': 'Bitir', 'down': '누르는중', 'exact': '정확한값', 'i': '순번', 'press': '글쇠누르기', 'rectangles': '사각형들', 'sym': 'nyşan', 'j': '안쪽순번', 'deadline': '마감시각', 'proc': 'Proses', 'data': 'maglumat', 'main': 'Bitir', 'w': '너비값', 'init': '초기값', 'block': 'maglumat_bökde', 'ROOT': '기준', 'text': 'Metin', 'marker': '확인표시', 'report': 'barlag_hasabat', 'until': '까지', 'clipboard': 'çalşyk_buferi_baha', 'dst': 'barylmaly_ýer_salgy', 'seen': '본항목들', 'poll': '준비살피미', 'transcript': '대화기록', 'port': '접속번호', 'offset': 'Süýşüriş_baha', 'h': '높이값', 'src': '원본주소', 'event': 'waka', 'encoding': 'nyşanlaryň_toplumy', 'size': 'Ululyk', 'key': '누름값', 'pixels': '화소들', 'y': '세로좌표', 'output': '출력결과', 'symbol': 'nyşan_baha', 'client': 'müşderi', 'char': 'nyşan_maglumat_4d9f8719', 'rgb': '빛삼원색'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
