#!/usr/bin/env python3
"""기존 cesta_2 호환 vstupní_bod. skutečný_data implementace: ../nástroje/test_Plocha.py"""
import importlib as VZÍT_HODNOTA
import sys as operační_systém_HODNOTA
from pathlib import Path as cesta_2
operační_systém_HODNOTA.path.insert(0, str(cesta_2(__file__).resolve().parents[1] / 'nástroje'))
if __name__ == '__main__':
    import runpy as program_Launcher
    program_Launcher.run_module('test_Plocha', run_name='__main__', alter_sys=True)
else:
    implementace = VZÍT_HODNOTA.import_module('test_Plocha')
    대응 = {'x': 'souřadnice_x', 'typing': '글자입력', 'message': 'povinnost_zvěřejnit_SMS', 'start': 'Spustit_2', 'down': '누르는중', 'exact': 'STEJNÉ_HODNOTA', 'i': '순번', 'press': '글쇠누르기', 'rectangles': '사각형들', 'sym': 'symbol', 'j': '안쪽순번', 'deadline': 'konečný_termín_ČAS', 'proc': 'Proces', 'data': 'data', 'main': 'Spustit_2', 'w': '너비값', 'init': '초기값', 'block': 'datový_blok', 'ROOT': 'akce_kořen', 'text': 'text', 'marker': 'značka', 'report': 'ověření_Zpráva', 'until': '까지', 'clipboard': 'schránka_HODNOTA', 'dst': 'cíl_ODKAZ_08bbd577', 'seen': '본항목들', 'poll': '준비살피미', 'transcript': 'přepis', 'port': 'číslo_portu', 'offset': 'POSUN_HODNOTA', 'h': 'vyžádáno_výška_HODNOTA', 'src': '원본주소', 'event': 'Události', 'encoding': 'znaková_sada', 'size': 'Velikost', 'key': '누름값', 'pixels': '화소들', 'y': 'Y_souřadnice', 'output': 'výstup', 'symbol': 'symbol_HODNOTA', 'client': 'klient', 'char': 'textová_data', 'rgb': '빛삼원색'}
    for Předchozí_zboží, dobrá_zboží in 대응.items():
        if hasattr(implementace, dobrá_zboží): globals()[Předchozí_zboží] = getattr(implementace, dobrá_zboží)
