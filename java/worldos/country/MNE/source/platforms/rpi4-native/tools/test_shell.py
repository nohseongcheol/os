#!/usr/bin/env python3
"""기존 putanja 호환 stavka_p. stvarni_podaci 구현: ../Alatke/셸시험.py"""
import importlib as TAKE_VALUE
import sys as operativni_sistem_VALUE
from pathlib import Path as putanja
operativni_sistem_VALUE.path.insert(0, str(putanja(__file__).resolve().parents[1] / 'Alatke'))
if __name__ == '__main__':
    import runpy as program_pokretač
    program_pokretač.run_module('셸시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('셸시험')
    mapiranje_VALUE = {'timeout': '시간제한', 'x': 'x_koordinata', 'msg': 'Mreža_poruka', 'i': '순번', 'reply': 'odgovor', 'call': '호출', 'args': 'argument_niz', 'chunk': '조각', 'data': 'podaci', 'proc': 'Proces', 'long_text': '긴글', 'restored': '복원자료', 'send': 'poslati', 'file': 'Datoteka', 'main': 'koristiti', 'found': 'SEARCH_KR', 'ROOT': 'radnja_koren', 'text': 'SMS', 'marker': 'označivač', 'command': 'komanda', 'expected': '예상결과', 'pixel': 'piksel', 'shell': 'ljuska', 'poll': '준비살피미', 'transcript': 'transkript', 'end': 'završiti_razgovor_Pomak', 'image': 'IMAGE', 'key': '누름값', 'y': '세로좌표', 'output': '출력결과', 'result': 'KR', 'client': 'klijent', 'line': 'red', 'stream': 'tok_VALUE', 'name': 'ime', 'value': 'VALUE', 'receive': 'primiti_poruka', 'report': 'provera_valjanosti_izveštaj', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, aktuelno_stavka in mapiranje_VALUE.items():
        if hasattr(구현, aktuelno_stavka): globals()[이전] = getattr(구현, aktuelno_stavka)
