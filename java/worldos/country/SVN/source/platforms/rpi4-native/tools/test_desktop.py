#!/usr/bin/env python3
"""기존 POT 호환 vnos_p. dejanski_podatki 구현: ../Orodja/preskusiti_namizje.py"""
import importlib as TAKE_VALUE
import sys as operacijski_sistem_VALUE
from pathlib import Path as POT
operacijski_sistem_VALUE.path.insert(0, str(POT(__file__).resolve().parents[1] / 'Orodja'))
if __name__ == '__main__':
    import runpy as aplikacija_zaganjalnik
    aplikacija_zaganjalnik.run_module('preskusiti_namizje', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('preskusiti_namizje')
    preslikava_VALUE = {'x': 'koordinata_x', 'typing': '글자입력', 'message': 'obvestilo_SMS', 'start': 'Zaženi', 'down': '누르는중', 'exact': 'EXACT_VALUE', 'i': '순번', 'press': 'pritisniti_Ključ', 'rectangles': '사각형들', 'sym': 'simbol', 'j': '안쪽순번', 'deadline': 'rok_čas', 'proc': 'Opravilo', 'data': 'podatki', 'main': 'Zaženi', 'w': '너비값', 'init': '초기값', 'block': 'blok_podatkov', 'ROOT': 'pobuda_koren', 'text': 'Besedilo', 'marker': 'oznaka', 'report': 'preverjanje_veljavnosti_prijavi', 'until': '까지', 'clipboard': 'odložišče_VALUE', 'dst': 'cilj_naslov_08bbd577', 'seen': '본항목들', 'poll': '준비살피미', 'transcript': 'prepis', 'port': 'številka_vrat', 'offset': 'odmik_VALUE', 'h': '높이값', 'src': '원본주소', 'event': 'dogodek', 'encoding': 'nabor_znakov', 'size': 'Velikost', 'key': '누름값', 'pixels': '화소들', 'y': '세로좌표', 'output': '출력결과', 'symbol': 'simbol_VALUE', 'client': 'odjemalec', 'char': 'znakovni_podatki', 'rgb': '빛삼원색'}
    for 이전, sprotno_element in preslikava_VALUE.items():
        if hasattr(구현, sprotno_element): globals()[이전] = getattr(구현, sprotno_element)
