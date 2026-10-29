#!/usr/bin/env python3
"""기존 Sti 호환 inngangspunkt. faktisk_data 구현: ../Verktøy/test_Swing.py"""
import importlib as TA_VERDI
import sys as operativsystem_VERDI
from pathlib import Path as Sti
operativsystem_VERDI.path.insert(0, str(Sti(__file__).resolve().parents[1] / 'Verktøy'))
if __name__ == '__main__':
    import runpy as app_appskuff
    app_appskuff.run_module('test_Swing', run_name='__main__', alter_sys=True)
else:
    구현 = TA_VERDI.import_module('test_Swing')
    tildeling_VERDI = {'wait': '기다리기', 'x': 'x_koordinat', 's': 'streng_data', 'i': '순번', 'sel': 'velger_a916db4e', 'seconds': '초단위', 'log': 'LOG_POST', 'data': 'data', 'at': 'betalt_plassere', 'send': 'sende', 'main': 'Kjør_2', 'req': 'forespørsel_VERDI', 'hot': 'alias_VERDI', 'pump': 'håndtak_hendelse', 'ROOT': 'speile_rot', 'marker': 'tusj', 'b': 'SEKUND_VERDI', 'command': 'Kommando', 'shell': 'Shell', 'f': 'Fil_oppføring', 'click': 'klikk_knapp', 'k': '셋째순번', 'c': 'tegnkode', 'r': '반환값', 'p': 'data_plassere', 'command_mode': 'kommando_MODUS', 'end': 'avslutte_en_samtale_FORSKYVNING', 'classes': 'time_bane', 'key': '누름값', 'y': 'Y_koordinat', 'result': 'KR', 'report': 'validering_rapport', 'dest': 'mål_VERDI_plassere', 'work': '작업경로', 'qmp': '모의제어접속'}
    for Forrige_vare, betalt_vare in tildeling_VERDI.items():
        if hasattr(구현, betalt_vare): globals()[Forrige_vare] = getattr(구현, betalt_vare)
