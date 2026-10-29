#!/usr/bin/env python3
"""기존 Cesta 호환 položka_bod. skutočný_údaje 구현: ../Nástroje/test_Windows.py"""
import importlib as TAKE_VALUE
import sys as operačný_systém_VALUE
from pathlib import Path as Cesta
operačný_systém_VALUE.path.insert(0, str(Cesta(__file__).resolve().parents[1] / 'Nástroje'))
if __name__ == '__main__':
    import runpy as program_spúšťač
    program_spúšťač.run_module('test_Windows', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('test_Windows')
    mapovanie_VALUE = {'wait': '기다리기', 'x': 'X_súradnica', 's': 'reťazec_údaje', 'xy': 'súradnice', 'sel': 'selektor_a916db4e', 'seconds': '초단위', 'log': 'LOG_RECORD', 'at': 'v_termíne_splatnosti_pozícia', 'send': 'odoslať', 'main': 'Spustiť_2', 'req': 'požiadavka_VALUE_625fa62c', 'hot': 'odkaz_VALUE_910d9d5a', 'pump': 'rukoväť_udalosť', 'ROOT': 'akcia_koreň', 'marker': 'fixka', 'b': 'SECOND_VALUE', 'command': 'Príkaz', 'shell': '셸', 'f': 'Súbor_položka', 'color': '색상', 'click': 'kliknúť_tlačidlo', 'k': '셋째순번', 'c': 'bod_kódu', 'r': '반환값', 'p': 'údaje_pozícia', 'done': 'Dokončené_úlohy_suma', 'end': 'ukončiť_hovor_Posun', 'command_mode': 'príkaz_MODE', 'key': '누름값', 'y': 'Y_súradnica', 'pixels': '화소들', 'result': 'KR', 'report': 'overenie_správa', 'dest': 'cieľ_VALUE_pozícia', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, v_termíne_splatnosti_položka in mapovanie_VALUE.items():
        if hasattr(구현, v_termíne_splatnosti_položka): globals()[이전] = getattr(구현, v_termíne_splatnosti_položka)
