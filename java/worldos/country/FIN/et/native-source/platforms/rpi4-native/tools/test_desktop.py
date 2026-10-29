#!/usr/bin/env python3
"""기존 RADA 호환 kirje_p. tegelik_andmed 구현: ../Tööriistad/바탕화면시험.py"""
import importlib as TAKE_VALUE
import sys as operatsioonisüsteem_VALUE
from pathlib import Path as RADA
operatsioonisüsteem_VALUE.path.insert(0, str(RADA(__file__).resolve().parents[1] / 'Tööriistad'))
if __name__ == '__main__':
    import runpy as programm_käiviti
    programm_käiviti.run_module('바탕화면시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('바탕화면시험')
    vastendamine_VALUE = {'x': '가로좌표', 'typing': '글자입력', 'message': 'teatamine_SMS', 'start': 'Käivita_2', 'down': '누르는중', 'exact': 'EXACT_VALUE', 'i': '순번', 'press': 'vajutama_Võti', 'rectangles': '사각형들', 'sym': 'sümbol', 'j': '안쪽순번', 'deadline': 'tähtaeg_Aeg', 'proc': 'Protsess', 'data': 'andmed', 'main': 'Käivita_2', 'w': '너비값', 'init': '초기값', 'block': 'andmeplokk', 'ROOT': 'Project_juur', 'text': 'Tekst', 'marker': 'marker', 'report': 'kinnitamine_aruanne', 'until': '까지', 'clipboard': 'lõikelaud_VALUE', 'dst': 'sihtkoht_ADDRESS', 'seen': '본항목들', 'poll': '준비살피미', 'transcript': 'transkriptsioon', 'port': 'pordinumber', 'offset': 'nihe_VALUE', 'h': '높이값', 'src': '원본주소', 'event': 'Sündmus', 'encoding': 'märgistik', 'size': 'Suurus', 'key': '누름값', 'pixels': '화소들', 'y': '세로좌표', 'output': 'toodang', 'symbol': 'sümbol_VALUE', 'client': 'klient', 'char': 'tähemärgiandmed', 'rgb': '빛삼원색'}
    for 이전, tähtaja_piires_kaup in vastendamine_VALUE.items():
        if hasattr(구현, tähtaja_piires_kaup): globals()[이전] = getattr(구현, tähtaja_piires_kaup)
