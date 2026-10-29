#!/usr/bin/env python3
"""기존 POT 호환 vnos_p. dejanski_podatki 구현: ../Orodja/preskusiti_Swing.py"""
import importlib as TAKE_VALUE
import sys as operacijski_sistem_VALUE
from pathlib import Path as POT
operacijski_sistem_VALUE.path.insert(0, str(POT(__file__).resolve().parents[1] / 'Orodja'))
if __name__ == '__main__':
    import runpy as aplikacija_zaganjalnik
    aplikacija_zaganjalnik.run_module('preskusiti_Swing', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('preskusiti_Swing')
    preslikava_VALUE = {'wait': '기다리기', 'x': 'koordinata_x', 's': 'niz_podatki', 'i': '순번', 'sel': 'izbirnik_a916db4e', 'seconds': '초단위', 'log': 'LOG_zapis', 'data': 'podatki', 'at': 'sprotno_položaj', 'send': 'poslati', 'main': 'Zaženi', 'req': 'zahteva_VALUE_625fa62c', 'hot': 'bližnjica_VALUE', 'pump': 'ročica_dogodek', 'ROOT': 'pobuda_koren', 'marker': 'oznaka', 'b': 'SECOND_VALUE', 'command': 'Ukaz', 'shell': 'lupina', 'f': 'Datoteka_vnos', 'click': 'klik_gumb', 'k': '셋째순번', 'c': 'koda_znaka', 'r': '반환값', 'p': 'podatki_položaj', 'command_mode': 'ukaz_MODE', 'end': 'končati_klic_odmik', 'classes': 'Razred_pot', 'key': '누름값', 'y': '세로좌표', 'result': 'REZULTAT', 'report': 'preverjanje_veljavnosti_prijavi', 'dest': 'cilj_VALUE_položaj', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, sprotno_element in preslikava_VALUE.items():
        if hasattr(구현, sprotno_element): globals()[이전] = getattr(구현, sprotno_element)
