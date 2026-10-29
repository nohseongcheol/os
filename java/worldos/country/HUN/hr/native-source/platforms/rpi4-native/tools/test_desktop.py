#!/usr/bin/env python3
"""기존 PUTANJA 호환 unos_p. stvaran_podaci 구현: ../Alati/바탕화면시험.py"""
import importlib as TAKE_VALUE
import sys as operacijski_sustav_VALUE
from pathlib import Path as PUTANJA
operacijski_sustav_VALUE.path.insert(0, str(PUTANJA(__file__).resolve().parents[1] / 'Alati'))
if __name__ == '__main__':
    import runpy as program_pokretač
    program_pokretač.run_module('바탕화면시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('바탕화면시험')
    mapiranje_VALUE = {'x': 'koordinata_x', 'typing': '글자입력', 'message': 'obavijest_SMS', 'start': 'Pokreni', 'down': '누르는중', 'exact': 'EXACT_VALUE', 'i': '순번', 'press': 'pritisnuti_Ključ', 'rectangles': '사각형들', 'sym': 'simbol', 'j': '안쪽순번', 'deadline': 'rok_za_dovršetak_TIME', 'proc': 'Proces', 'data': 'podaci', 'main': 'Pokreni', 'w': '너비값', 'init': '초기값', 'block': 'podatkovni_blok', 'ROOT': 'akcija_korijen', 'text': 'Tekst', 'marker': 'marker', 'report': 'provjera_izvješće', 'until': '까지', 'clipboard': 'međuspremnik_VALUE', 'dst': 'odredište_adresa', 'seen': '본항목들', 'poll': '준비살피미', 'transcript': 'transkript', 'port': 'broj_priključka', 'offset': 'pomak_VALUE', 'h': '높이값', 'src': '원본주소', 'event': 'Događaj', 'encoding': 'skup_znakova', 'size': 'Veličina', 'key': '누름값', 'pixels': '화소들', 'y': '세로좌표', 'output': '출력결과', 'symbol': 'simbol_VALUE', 'client': 'klijent', 'char': 'znakovni_podaci', 'rgb': '빛삼원색'}
    for 이전, redovno_artikl in mapiranje_VALUE.items():
        if hasattr(구현, redovno_artikl): globals()[이전] = getattr(구현, redovno_artikl)
