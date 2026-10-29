#!/usr/bin/env python3
"""기존 putanja 호환 stavka_p. stvarni_podaci 구현: ../Alatke/바탕화면시험.py"""
import importlib as TAKE_VALUE
import sys as operativni_sistem_VALUE
from pathlib import Path as putanja
operativni_sistem_VALUE.path.insert(0, str(putanja(__file__).resolve().parents[1] / 'Alatke'))
if __name__ == '__main__':
    import runpy as program_pokretač
    program_pokretač.run_module('바탕화면시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('바탕화면시험')
    mapiranje_VALUE = {'x': 'x_koordinata', 'typing': '글자입력', 'message': 'obaveštavanje_SMS', 'start': 'koristiti', 'down': '누르는중', 'exact': 'EXACT_VALUE', 'i': '순번', 'press': 'pritisnuti_Ključ', 'rectangles': '사각형들', 'sym': 'simbol', 'j': '안쪽순번', 'deadline': 'krajnji_rok_TIME', 'proc': 'Proces', 'data': 'podaci', 'main': 'koristiti', 'w': '너비값', 'init': '초기값', 'block': 'blok_podataka', 'ROOT': 'radnja_koren', 'text': 'SMS', 'marker': 'označivač', 'report': 'provera_valjanosti_izveštaj', 'until': '까지', 'clipboard': 'međuspremnik_VALUE', 'dst': 'odredište_adresa', 'seen': '본항목들', 'poll': '준비살피미', 'transcript': 'transkript', 'port': 'broj_porta', 'offset': 'Pomak_VALUE', 'h': '높이값', 'src': '원본주소', 'event': 'događaj', 'encoding': 'skup_znakova', 'size': 'promeniti_veličinu', 'key': '누름값', 'pixels': '화소들', 'y': '세로좌표', 'output': '출력결과', 'symbol': 'simbol_VALUE', 'client': 'klijent', 'char': 'znakovni_podaci', 'rgb': '빛삼원색'}
    for 이전, aktuelno_stavka in mapiranje_VALUE.items():
        if hasattr(구현, aktuelno_stavka): globals()[이전] = getattr(구현, aktuelno_stavka)
