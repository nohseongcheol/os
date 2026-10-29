#!/usr/bin/env python3
"""기존 Cığır 호환 daxiletmə_p. faktiki_verilənlər 구현: ../Alətlər/바탕화면시험.py"""
import importlib as TAKE_VALUE
import sys as əməliyyat_sistemi_VALUE
from pathlib import Path as Cığır
əməliyyat_sistemi_VALUE.path.insert(0, str(Cığır(__file__).resolve().parents[1] / 'Alətlər'))
if __name__ == '__main__':
    import runpy as proqram_işəsalma
    proqram_işəsalma.run_module('바탕화면시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('바탕화면시험')
    대응 = {'x': 'x_koordinatı', 'typing': '글자입력', 'message': '알림문', 'start': 'İcra_Et', 'down': '누르는중', 'exact': 'EXACT_VALUE', 'i': '순번', 'press': 'bas_Açar', 'rectangles': '사각형들', 'sym': 'simvol', 'j': '안쪽순번', 'deadline': '마감시각', 'proc': 'Proses', 'data': 'verilənlər', 'main': 'İcra_Et', 'w': '너비값', 'init': '초기값', 'block': 'verilənlər_blokla', 'ROOT': 'Project_kök', 'text': 'Mətn', 'marker': '확인표시', 'report': 'yoxlama_hesabat', 'until': '까지', 'clipboard': 'mübadilə_buferi_VALUE', 'dst': 'təyinat_ünvan', 'seen': '본항목들', 'poll': '준비살피미', 'transcript': '대화기록', 'port': '접속번호', 'offset': 'OFFSET_VALUE', 'h': '높이값', 'src': '원본주소', 'event': 'hadisə', 'encoding': 'simvol_dəsti', 'size': 'Böyüklük', 'key': '누름값', 'pixels': '화소들', 'y': 'Y_koordinat', 'output': '출력결과', 'symbol': 'simvol_VALUE', 'client': 'müştəri', 'char': 'simvol_verilənlər_4d9f8719', 'rgb': '빛삼원색'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
