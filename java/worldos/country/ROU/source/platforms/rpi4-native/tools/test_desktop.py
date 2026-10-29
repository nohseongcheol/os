#!/usr/bin/env python3
"""기존 Cale 호환 intrare_p. real_date 구현: ../Instrumente/바탕화면시험.py"""
import importlib as TAKE_VALUE
import sys as sistem_de_operare_VALUE
from pathlib import Path as Cale
sistem_de_operare_VALUE.path.insert(0, str(Cale(__file__).resolve().parents[1] / 'Instrumente'))
if __name__ == '__main__':
    import runpy as program_ecrane_de_lansare
    program_ecrane_de_lansare.run_module('바탕화면시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('바탕화면시험')
    mapare_VALUE = {'x': 'coordonata_X', 'typing': '글자입력', 'message': 'înștiințare_SMS', 'start': 'Pornește', 'down': '누르는중', 'exact': 'EXACT_VALUE', 'i': '순번', 'press': 'apăsa_Cheie', 'rectangles': '사각형들', 'sym': 'simbol', 'j': '안쪽순번', 'deadline': 'dată_limită_oră', 'proc': 'Proces', 'data': 'date', 'main': 'Pornește', 'w': '너비값', 'init': '초기값', 'block': 'bloc_de_date', 'ROOT': 'Project_rădăcină', 'text': 'SMS', 'marker': 'marcaj', 'report': 'validare_raport', 'until': '까지', 'clipboard': 'clipboard_VALUE', 'dst': 'destinație_adresa', 'seen': '본항목들', 'poll': '준비살피미', 'transcript': 'transcriere', 'port': 'număr_port', 'offset': 'OFFSET_VALUE', 'h': '높이값', 'src': '원본주소', 'event': 'Eveniment', 'encoding': 'set_de_caractere', 'size': 'Mărime', 'key': '누름값', 'pixels': '화소들', 'y': '세로좌표', 'output': '출력결과', 'symbol': 'simbol_VALUE', 'client': 'client', 'char': 'date_de_tip_caracter', 'rgb': '빛삼원색'}
    for Anteriorul_element, curent_element in mapare_VALUE.items():
        if hasattr(구현, curent_element): globals()[Anteriorul_element] = getattr(구현, curent_element)
