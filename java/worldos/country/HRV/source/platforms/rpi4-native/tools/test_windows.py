#!/usr/bin/env python3
"""기존 PUTANJA 호환 unos_p. stvaran_podaci 구현: ../Alati/창시험.py"""
import importlib as TAKE_VALUE
import sys as operacijski_sustav_VALUE
from pathlib import Path as PUTANJA
operacijski_sustav_VALUE.path.insert(0, str(PUTANJA(__file__).resolve().parents[1] / 'Alati'))
if __name__ == '__main__':
    import runpy as program_pokretač
    program_pokretač.run_module('창시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('창시험')
    mapiranje_VALUE = {'wait': '기다리기', 'x': 'koordinata_x', 's': 'niz_podaci', 'xy': 'koordinirani_par', 'sel': 'odabirač_a916db4e', 'seconds': '초단위', 'log': 'LOG_zapis', 'at': 'redovno_položaj', 'send': 'slati', 'main': 'Pokreni', 'req': 'zahtjev_VALUE', 'hot': 'prečac_VALUE', 'pump': 'ustroj_događaj', 'ROOT': 'akcija_korijen', 'marker': 'marker', 'b': 'SECOND_VALUE', 'command': 'Naredba', 'shell': 'ljuska', 'f': 'Datoteka_unos', 'color': '색상', 'click': 'klik_tipka', 'k': '셋째순번', 'c': 'kodna_točka', 'r': '반환값', 'p': 'podaci_položaj', 'done': 'Dovršeno_iznos', 'end': 'završiti_razgovor_pomak', 'command_mode': 'naredba_MODE', 'key': '누름값', 'y': '세로좌표', 'pixels': '화소들', 'result': 'REZULTAT', 'report': 'provjera_izvješće', 'dest': 'odredište_VALUE_položaj', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, redovno_artikl in mapiranje_VALUE.items():
        if hasattr(구현, redovno_artikl): globals()[이전] = getattr(구현, redovno_artikl)
