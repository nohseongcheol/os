#!/usr/bin/env python3
"""기존 Bide_izena 호환 sarrera_p. benetako_datuak 구현: ../Tresnak/바탕화면시험.py"""
import importlib as HARTU_balio
import sys as sistema_eragile_balio
from pathlib import Path as Bide_izena
sistema_eragile_balio.path.insert(0, str(Bide_izena(__file__).resolve().parents[1] / 'Tresnak'))
if __name__ == '__main__':
    import runpy as aplik_abiarazle
    aplik_abiarazle.run_module('바탕화면시험', run_name='__main__', alter_sys=True)
else:
    구현 = HARTU_balio.import_module('바탕화면시험')
    대응 = {'x': 'X_koordenatu', 'typing': '글자입력', 'message': '알림문', 'start': 'Exekutatu_2', 'down': '누르는중', 'exact': 'BERDIN_balio', 'i': '순번', 'press': 'sakatu_gako', 'rectangles': '사각형들', 'sym': 'ikur', 'j': '안쪽순번', 'deadline': '마감시각', 'proc': 'Prozesua', 'data': 'datuak', 'main': 'Exekutatu_2', 'w': '너비값', 'init': '초기값', 'block': 'datuak_blokeatu', 'ROOT': 'Project_erro', 'text': 'Testua', 'marker': '확인표시', 'report': 'balidazio_txosten', 'until': '까지', 'clipboard': 'arbel_balio', 'dst': 'helburu_helbide_08bbd577', 'seen': '본항목들', 'poll': '준비살피미', 'transcript': '대화기록', 'port': 'ataka_zenbaki', 'offset': 'Geruzak_balio', 'h': '높이값', 'src': '원본주소', 'event': 'Gertaera', 'encoding': 'karaktere_joko', 'size': 'Tamaina', 'key': '누름값', 'pixels': '화소들', 'y': 'Y_koordenatu', 'output': '출력결과', 'symbol': 'ikur_balio', 'client': 'bezero', 'char': 'karaktere_datuak', 'rgb': '빛삼원색'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
