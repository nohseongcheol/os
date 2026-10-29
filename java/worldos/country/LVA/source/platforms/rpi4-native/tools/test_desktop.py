#!/usr/bin/env python3
"""기존 CEĻŠ 호환 ieejas_punkts. faktisks_dati 구현: ../Rīki/바탕화면시험.py"""
import importlib as TAKE_VALUE
import sys as operētājsistēma_VALUE
from pathlib import Path as CEĻŠ
operētājsistēma_VALUE.path.insert(0, str(CEĻŠ(__file__).resolve().parents[1] / 'Rīki'))
if __name__ == '__main__':
    import runpy as programma_palaidējs
    programma_palaidējs.run_module('바탕화면시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('바탕화면시험')
    kartēšana_VALUE = {'x': 'x_koordināta', 'typing': '글자입력', 'message': 'informēšana_SMS', 'start': 'Palaist', 'down': '누르는중', 'exact': 'EXACT_VALUE', 'i': '순번', 'press': 'nospiest_Atslēga', 'rectangles': '사각형들', 'sym': 'simbols', 'j': '안쪽순번', 'deadline': 'izpildes_termiņš_TIME', 'proc': 'Process', 'data': 'dati', 'main': 'Palaist', 'w': '너비값', 'init': '초기값', 'block': 'datu_bloks', 'ROOT': 'Project_sakne', 'text': 'Teksts', 'marker': 'marķieris', 'report': 'validācija_ziņot', 'until': '까지', 'clipboard': 'starpliktuve_VALUE', 'dst': 'mērķis_adrese_08bbd577', 'seen': '본항목들', 'poll': '준비살피미', 'transcript': 'transkripcija', 'port': 'porta_numurs', 'offset': 'Nobīde_VALUE', 'h': '높이값', 'src': '원본주소', 'event': 'Notikums', 'encoding': 'rakstzīmju_kopa', 'size': 'Izmērs', 'key': '누름값', 'pixels': '화소들', 'y': '세로좌표', 'output': 'ražojums', 'symbol': 'simbols_VALUE', 'client': 'klients', 'char': 'rakstzīmju_dati', 'rgb': '빛삼원색'}
    for 이전, pašreizējais_krājums in kartēšana_VALUE.items():
        if hasattr(구현, pašreizējais_krājums): globals()[이전] = getattr(구현, pašreizējais_krājums)
