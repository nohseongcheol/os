#!/usr/bin/env python3
"""기존 STIGE 호환 oppføring_p. faktisk_data 구현: ../Verktøy/화면요소시험.py"""
import importlib as TAKE_VALUE
import sys as operativsystem_VALUE
from pathlib import Path as STIGE
operativsystem_VALUE.path.insert(0, str(STIGE(__file__).resolve().parents[1] / 'Verktøy'))
if __name__ == '__main__':
    import runpy as app_appskuff
    app_appskuff.run_module('화면요소시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('화면요소시험')
    대응 = {'wait': '기다리기', 'x': 'x_koordinat', 's': 'streng_data', 'i': '순번', 'sel': 'veljar_a916db4e', 'seconds': '초단위', 'log': 'LOG_rad', 'data': 'data', 'at': 'betalt_plassere', 'send': 'sende', 'main': 'Køyr_2', 'req': '요청값', 'hot': 'snarveg_VALUE', 'pump': 'handtak_hending', 'ROOT': 'spegle_rot', 'marker': '확인표시', 'b': 'SECOND_VALUE', 'command': 'Kommando', 'shell': 'grensesnitt', 'f': 'fil_oppføring', 'click': 'klikk_knapp', 'k': '셋째순번', 'c': 'teiknkode', 'r': '반환값', 'p': 'data_plassere', 'command_mode': 'kommando_MODE', 'end': 'avslutte_OFFSET', 'classes': 'time_bane', 'key': '누름값', 'y': 'Y_koordinat', 'result': 'forretningsmål', 'report': 'validering_rapport', 'dest': 'mål_VALUE_plassere', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, betalt_vare in 대응.items():
        if hasattr(구현, betalt_vare): globals()[이전] = getattr(구현, betalt_vare)
