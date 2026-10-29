#!/usr/bin/env python3
"""기존 SLÓÐ 호환 færsla_P. raun_gögn 구현: ../Verkfæri/창시험.py"""
import importlib as TAKE_VALUE
import sys as stýrikerfi_VALUE
from pathlib import Path as SLÓÐ
stýrikerfi_VALUE.path.insert(0, str(SLÓÐ(__file__).resolve().parents[1] / 'Verkfæri'))
if __name__ == '__main__':
    import runpy as forrit_ræsir
    forrit_ræsir.run_module('창시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('창시험')
    vörpun_VALUE = {'wait': '기다리기', 'x': 'x_hnit', 's': 'strengur_gögn', 'xy': 'hnitapar', 'sel': 'val_a916db4e', 'seconds': '초단위', 'log': 'LOG_lína', 'at': '현재위치', 'send': 'senda', 'main': 'Keyra_2', 'req': '요청값', 'hot': 'flýtileið_VALUE', 'pump': 'hald_atvik', 'ROOT': 'verk_rót', 'marker': '확인표시', 'b': 'SECOND_VALUE', 'command': 'Skipun', 'shell': 'skel', 'f': 'skrá_færsla_3d0c1245', 'color': '색상', 'click': 'smella_hnappur', 'k': '셋째순번', 'c': 'stafkóði', 'r': '반환값', 'p': 'gögn_staða', 'done': 'lokið_upphæð', 'end': 'ljúka_OFFSET', 'command_mode': 'skipun_MODE', 'key': '누름값', 'y': 'Y_hnit', 'pixels': '화소들', 'result': 'NIÐURSTAÐA', 'report': 'prófun_skrá', 'dest': 'endastaður_VALUE_staða', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in vörpun_VALUE.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
