#!/usr/bin/env python3
"""기존 PUTANJA 호환 unos_p. stvaran_podaci 구현: ../Alati/셸시험.py"""
import importlib as TAKE_VALUE
import sys as operacijski_sustav_VALUE
from pathlib import Path as PUTANJA
operacijski_sustav_VALUE.path.insert(0, str(PUTANJA(__file__).resolve().parents[1] / 'Alati'))
if __name__ == '__main__':
    import runpy as program_pokretač
    program_pokretač.run_module('셸시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('셸시험')
    mapiranje_VALUE = {'timeout': '시간제한', 'x': 'koordinata_x', 'msg': 'mreža_poruka', 'i': '순번', 'reply': 'odgovor', 'call': '호출', 'args': 'argument_ARRAY', 'chunk': 'fragment_VALUE', 'data': 'podaci', 'proc': 'Proces', 'long_text': '긴글', 'restored': '복원자료', 'send': 'slati', 'file': 'Datoteka', 'main': 'Pokreni', 'found': 'Traži_KR', 'ROOT': 'akcija_korijen', 'text': 'Tekst', 'marker': 'marker', 'command': 'Naredba', 'expected': '예상결과', 'pixel': 'slikovni_element', 'shell': 'ljuska', 'poll': '준비살피미', 'transcript': 'transkript', 'end': 'završiti_razgovor_pomak', 'image': 'IMAGE', 'key': '누름값', 'y': '세로좌표', 'output': '출력결과', 'result': 'REZULTAT', 'client': 'klijent', 'line': 'red', 'stream': 'tok_VALUE', 'name': 'Ime', 'value': 'VALUE', 'receive': 'primiti_poruka', 'report': 'provjera_izvješće', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, redovno_artikl in mapiranje_VALUE.items():
        if hasattr(구현, redovno_artikl): globals()[이전] = getattr(구현, redovno_artikl)
