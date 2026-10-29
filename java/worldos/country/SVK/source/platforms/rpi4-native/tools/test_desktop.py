#!/usr/bin/env python3
"""기존 Cesta 호환 položka_bod. skutočný_údaje 구현: ../Nástroje/test_počítač.py"""
import importlib as TAKE_VALUE
import sys as operačný_systém_VALUE
from pathlib import Path as Cesta
operačný_systém_VALUE.path.insert(0, str(Cesta(__file__).resolve().parents[1] / 'Nástroje'))
if __name__ == '__main__':
    import runpy as program_spúšťač
    program_spúšťač.run_module('test_počítač', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('test_počítač')
    mapovanie_VALUE = {'x': 'X_súradnica', 'typing': '글자입력', 'message': 'upozornenie_SMS', 'start': 'Spustiť_2', 'down': '누르는중', 'exact': 'EXACT_VALUE', 'i': '순번', 'press': '글쇠누르기', 'rectangles': '사각형들', 'sym': 'symbol', 'j': '안쪽순번', 'deadline': 'termín_čas', 'proc': 'Proces', 'data': 'údaje', 'main': 'Spustiť_2', 'w': '너비값', 'init': '초기값', 'block': 'blok_údajov', 'ROOT': 'akcia_koreň', 'text': 'Spracovanie_textu', 'marker': 'fixka', 'report': 'overenie_správa', 'until': '까지', 'clipboard': 'Schránka_VALUE', 'dst': 'cieľ_adresa_08bbd577', 'seen': '본항목들', 'poll': '준비살피미', 'transcript': 'prepis', 'port': 'číslo_portu', 'offset': 'Posun_VALUE', 'h': '높이값', 'src': '원본주소', 'event': 'Udalosť', 'encoding': 'tabuľka_znakov', 'size': 'Veľkosť', 'key': '누름값', 'pixels': '화소들', 'y': 'Y_súradnica', 'output': '출력결과', 'symbol': 'symbol_VALUE', 'client': 'klient', 'char': 'znakové_údaje', 'rgb': '빛삼원색'}
    for 이전, v_termíne_splatnosti_položka in mapovanie_VALUE.items():
        if hasattr(구현, v_termíne_splatnosti_položka): globals()[이전] = getattr(구현, v_termíne_splatnosti_položka)
