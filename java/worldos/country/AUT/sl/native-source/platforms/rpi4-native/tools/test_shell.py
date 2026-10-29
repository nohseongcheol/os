#!/usr/bin/env python3
"""기존 POT 호환 vnos_p. dejanski_podatki 구현: ../Orodja/preskusiti_lupina.py"""
import importlib as TAKE_VALUE
import sys as operacijski_sistem_VALUE
from pathlib import Path as POT
operacijski_sistem_VALUE.path.insert(0, str(POT(__file__).resolve().parents[1] / 'Orodja'))
if __name__ == '__main__':
    import runpy as aplikacija_zaganjalnik
    aplikacija_zaganjalnik.run_module('preskusiti_lupina', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('preskusiti_lupina')
    preslikava_VALUE = {'timeout': '시간제한', 'x': 'koordinata_x', 'msg': 'mreža_e_pošta', 'i': '순번', 'reply': 'odgovor', 'call': '호출', 'args': 'argument_ARRAY', 'chunk': '조각', 'data': 'podatki', 'proc': 'Opravilo', 'long_text': '긴글', 'restored': '복원자료', 'send': 'poslati', 'file': 'Datoteka', 'main': 'Zaženi', 'found': 'Išči_KR', 'ROOT': 'pobuda_koren', 'text': 'Besedilo', 'marker': 'oznaka', 'command': 'Ukaz', 'expected': '예상결과', 'pixel': 'slikovna_pika', 'shell': 'lupina', 'poll': '준비살피미', 'transcript': 'prepis', 'end': 'končati_klic_odmik', 'image': 'IMAGE', 'key': '누름값', 'y': '세로좌표', 'output': '출력결과', 'result': 'REZULTAT', 'client': 'odjemalec', 'line': 'Črtni', 'stream': 'tok_VALUE', 'name': 'Ime', 'value': 'VALUE', 'receive': 'sprejeti_sprejemati_prejeti_prejemati_e_pošta', 'report': 'preverjanje_veljavnosti_prijavi', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, sprotno_element in preslikava_VALUE.items():
        if hasattr(구현, sprotno_element): globals()[이전] = getattr(구현, sprotno_element)
