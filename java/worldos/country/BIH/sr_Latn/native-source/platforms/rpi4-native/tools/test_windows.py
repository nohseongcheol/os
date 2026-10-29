#!/usr/bin/env python3
"""기존 putanja 호환 stavka_p. stvarni_podaci 구현: ../Alatke/창시험.py"""
import importlib as TAKE_VALUE
import sys as operativni_sistem_VALUE
from pathlib import Path as putanja
operativni_sistem_VALUE.path.insert(0, str(putanja(__file__).resolve().parents[1] / 'Alatke'))
if __name__ == '__main__':
    import runpy as program_pokretač
    program_pokretač.run_module('창시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('창시험')
    mapiranje_VALUE = {'wait': '기다리기', 'x': 'x_koordinata', 's': 'niska_podaci', 'xy': 'koordinatni_par', 'sel': 'birač_a916db4e', 'seconds': '초단위', 'log': 'LOG_snimi', 'at': 'aktuelno_pozicija', 'send': 'poslati', 'main': 'koristiti', 'req': 'zahtev_VALUE_625fa62c', 'hot': 'prečica_VALUE', 'pump': 'pokazivač_događaj', 'ROOT': 'radnja_koren', 'marker': 'označivač', 'b': 'SECOND_VALUE', 'command': 'komanda', 'shell': 'ljuska', 'f': 'Datoteka_stavka', 'color': '색상', 'click': 'klik_taster', 'k': '셋째순번', 'c': 'kôd_znaka', 'r': '반환값', 'p': 'podaci_pozicija', 'done': 'Dovršeno_iznos', 'end': 'završiti_razgovor_Pomak', 'command_mode': 'komanda_MODE', 'key': '누름값', 'y': '세로좌표', 'pixels': '화소들', 'result': 'KR', 'report': 'provera_valjanosti_izveštaj', 'dest': 'odredište_VALUE_pozicija', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, aktuelno_stavka in mapiranje_VALUE.items():
        if hasattr(구현, aktuelno_stavka): globals()[이전] = getattr(구현, aktuelno_stavka)
