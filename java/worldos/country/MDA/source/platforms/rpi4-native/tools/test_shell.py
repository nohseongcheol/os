#!/usr/bin/env python3
"""기존 Cale 호환 intrare_p. real_date 구현: ../Instrumente/셸시험.py"""
import importlib as TAKE_VALUE
import sys as sistem_de_operare_VALUE
from pathlib import Path as Cale
sistem_de_operare_VALUE.path.insert(0, str(Cale(__file__).resolve().parents[1] / 'Instrumente'))
if __name__ == '__main__':
    import runpy as program_ecrane_de_lansare
    program_ecrane_de_lansare.run_module('셸시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('셸시험')
    mapare_VALUE = {'timeout': 'executare_TIMEOUT', 'x': 'coordonata_X', 'msg': 'rețea_mesaj', 'i': '순번', 'reply': 'replică', 'call': '호출', 'args': 'argument_ARRAY', 'chunk': '조각', 'data': 'date', 'proc': 'Proces', 'long_text': '긴글', 'restored': '복원자료', 'send': 'trimite', 'file': 'Fișier', 'main': 'Pornește', 'found': 'căuta_KR', 'ROOT': 'Project_rădăcină', 'text': 'SMS', 'marker': 'marcaj', 'command': 'Comandă', 'expected': '예상결과', 'pixel': 'element_imagine', 'shell': 'shell', 'poll': '준비살피미', 'transcript': 'transcriere', 'end': 'termina_un_apel_OFFSET', 'image': 'IMAGE', 'key': '누름값', 'y': '세로좌표', 'output': '출력결과', 'result': 'KR', 'client': 'client', 'line': 'Linie', 'stream': 'flux_VALUE', 'name': 'Nume', 'value': 'VALUE', 'receive': 'primi_mesaj', 'report': 'validare_raport', 'work': '작업경로', 'qmp': '모의제어접속'}
    for Anteriorul_element, curent_element in mapare_VALUE.items():
        if hasattr(구현, curent_element): globals()[Anteriorul_element] = getattr(구현, curent_element)
