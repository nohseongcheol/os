#!/usr/bin/env python3
"""기존 Putanja 호환 unos_p. stvaran_podaci 구현: ../Alati/화면요소시험.py"""
import importlib as TAKE_VALUE
import sys as operativni_sistem_VALUE
from pathlib import Path as Putanja
operativni_sistem_VALUE.path.insert(0, str(Putanja(__file__).resolve().parents[1] / 'Alati'))
if __name__ == '__main__':
    import runpy as program_pokretač
    program_pokretač.run_module('화면요소시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('화면요소시험')
    대응 = {'wait': '기다리기', 'x': 'koordinata_x', 's': 'string_podaci', 'i': '순번', 'sel': 'birač_a916db4e', 'seconds': '초단위', 'log': 'LOG_red', 'data': 'podaci', 'at': 'trenutno_položaj', 'send': 'poslati', 'main': 'Pokreni', 'req': 'HTTP_zahtjev_VALUE', 'hot': 'prečica_VALUE', 'pump': 'hvatište_događaj', 'ROOT': 'projicirati_koijen', 'marker': '확인표시', 'b': 'SECOND_VALUE', 'command': 'Naredba', 'shell': 'ljuska', 'f': 'fajl_unos', 'click': 'klik_dugme', 'k': '셋째순번', 'c': 'kôd_znaka', 'r': '반환값', 'p': 'podaci_položaj', 'command_mode': 'komanda_mod', 'end': 'završiti_Pomak', 'classes': 'klasa_put', 'key': '누름값', 'y': 'Y_koordinata', 'result': 'mjera', 'report': 'provjera_izvještaj', 'dest': 'odredište_VALUE_položaj', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, trenutno_stavka in 대응.items():
        if hasattr(구현, trenutno_stavka): globals()[이전] = getattr(구현, trenutno_stavka)
