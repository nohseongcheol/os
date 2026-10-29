#!/usr/bin/env python3
"""기존 ÚTVONAL 호환 belépési_pont. tényleges_adat 구현: ../Eszközök/teszt_Windows.py"""
import importlib as ÁTHELYEZ_ÉRTÉK
import sys as operációs_rendszer_ÉRTÉK
from pathlib import Path as ÚTVONAL
operációs_rendszer_ÉRTÉK.path.insert(0, str(ÚTVONAL(__file__).resolve().parents[1] / 'Eszközök'))
if __name__ == '__main__':
    import runpy as app_indító
    app_indító.run_module('teszt_Windows', run_name='__main__', alter_sys=True)
else:
    구현 = ÁTHELYEZ_ÉRTÉK.import_module('teszt_Windows')
    leképezés_ÉRTÉK = {'wait': '기다리기', 'x': 'x_koordináta', 's': 'sztring_adat', 'xy': 'koordinátapár', 'sel': 'szelektor_a916db4e', 'seconds': '초단위', 'log': 'LOG_REKORD', 'at': 'aktuális_pozíció', 'send': 'küld', 'main': 'Futtatás', 'req': 'kérés_ÉRTÉK', 'hot': 'hivatkozás_ÉRTÉK', 'pump': 'leíró_esemény', 'ROOT': 'teendő_gyök', 'marker': 'jelölő', 'b': 'MPERC_ÉRTÉK', 'command': 'Parancs', 'shell': 'felület', 'f': 'Fájl_bejegyzés', 'color': '색상', 'click': 'kattint_gomb', 'k': '셋째순번', 'c': 'kódpont', 'r': '반환값', 'p': 'adat_pozíció', 'done': 'Kész_összeg', 'end': 'megszüntet_Ofszet', 'command_mode': 'parancs_mód', 'key': '누름값', 'y': 'Y_koordináta', 'pixels': '화소들', 'result': 'KR', 'report': 'ellenőrzés_jelent', 'dest': 'cél_ÉRTÉK_pozíció', 'work': '작업경로', 'qmp': '모의제어접속'}
    for Előző_cikk, aktuális_cikk in leképezés_ÉRTÉK.items():
        if hasattr(구현, aktuális_cikk): globals()[Előző_cikk] = getattr(구현, aktuális_cikk)
