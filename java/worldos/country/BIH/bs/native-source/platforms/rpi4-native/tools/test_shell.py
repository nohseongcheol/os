#!/usr/bin/env python3
"""기존 Putanja 호환 unos_p. stvaran_podaci 구현: ../Alati/셸시험.py"""
import importlib as TAKE_VALUE
import sys as operativni_sistem_VALUE
from pathlib import Path as Putanja
operativni_sistem_VALUE.path.insert(0, str(Putanja(__file__).resolve().parents[1] / 'Alati'))
if __name__ == '__main__':
    import runpy as program_pokretač
    program_pokretač.run_module('셸시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('셸시험')
    대응 = {'timeout': '시간제한', 'x': 'koordinata_x', 'msg': 'Mreža_poruka', 'i': '순번', 'reply': 'odgovoriti', 'call': '호출', 'args': 'argument_niz', 'chunk': '조각', 'data': 'podaci', 'proc': 'proces', 'long_text': '긴글', 'restored': '복원자료', 'send': 'poslati', 'file': 'Fajl', 'main': 'Pokreni', 'found': 'Traži_mjera', 'ROOT': 'projicirati_koijen', 'text': 'Tekst', 'marker': '확인표시', 'command': 'Naredba', 'expected': '예상결과', 'pixel': 'pel', 'shell': 'ljuska', 'poll': '준비살피미', 'transcript': '대화기록', 'end': 'završiti_Pomak', 'image': 'IMAGE', 'key': '누름값', 'y': 'Y_koordinata', 'output': '출력결과', 'result': 'mjera', 'client': 'klijent', 'line': 'Linija', 'stream': 'tok_VALUE', 'name': 'Naziv', 'value': 'VALUE', 'receive': '수신하기', 'report': 'provjera_izvještaj', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, trenutno_stavka in 대응.items():
        if hasattr(구현, trenutno_stavka): globals()[이전] = getattr(구현, trenutno_stavka)
