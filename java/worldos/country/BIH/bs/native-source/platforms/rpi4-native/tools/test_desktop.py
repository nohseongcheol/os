#!/usr/bin/env python3
"""기존 Putanja 호환 unos_p. stvaran_podaci 구현: ../Alati/바탕화면시험.py"""
import importlib as TAKE_VALUE
import sys as operativni_sistem_VALUE
from pathlib import Path as Putanja
operativni_sistem_VALUE.path.insert(0, str(Putanja(__file__).resolve().parents[1] / 'Alati'))
if __name__ == '__main__':
    import runpy as program_pokretač
    program_pokretač.run_module('바탕화면시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('바탕화면시험')
    대응 = {'x': 'koordinata_x', 'typing': '글자입력', 'message': '알림문', 'start': 'Pokreni', 'down': '누르는중', 'exact': 'EXACT_VALUE', 'i': '순번', 'press': 'pritisnuti_ključ', 'rectangles': '사각형들', 'sym': 'simbol', 'j': '안쪽순번', 'deadline': '마감시각', 'proc': 'proces', 'data': 'podaci', 'main': 'Pokreni', 'w': '너비값', 'init': '초기값', 'block': 'podaci_blokirati', 'ROOT': 'projicirati_koijen', 'text': 'Tekst', 'marker': '확인표시', 'report': 'provjera_izvještaj', 'until': '까지', 'clipboard': 'međuspremnik_VALUE', 'dst': 'odredište_adresa', 'seen': '본항목들', 'poll': '준비살피미', 'transcript': '대화기록', 'port': 'broj_priključka', 'offset': 'Pomak_VALUE', 'h': '높이값', 'src': '원본주소', 'event': 'događaj', 'encoding': 'skup_znakova', 'size': 'Veličina', 'key': '누름값', 'pixels': '화소들', 'y': 'Y_koordinata', 'output': '출력결과', 'symbol': 'simbol_VALUE', 'client': 'klijent', 'char': 'znak_podaci', 'rgb': '빛삼원색'}
    for 이전, trenutno_stavka in 대응.items():
        if hasattr(구현, trenutno_stavka): globals()[이전] = getattr(구현, trenutno_stavka)
