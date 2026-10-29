#!/usr/bin/env python3
"""기존 mogħdija 호환 entrata_punt. attwali_data 구현: ../Għodod/창시험.py"""
import importlib as TAKE_VALUE
import sys as sistema_operattiva_VALUE
from pathlib import Path as mogħdija
sistema_operattiva_VALUE.path.insert(0, str(mogħdija(__file__).resolve().parents[1] / 'Għodod'))
if __name__ == '__main__':
    import runpy as programm_ġabra_ta_apps
    programm_ġabra_ta_apps.run_module('창시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('창시험')
    대응 = {'wait': '기다리기', 'x': 'koordinat_x', 's': 'string_data', 'xy': 'par_koordinati', 'sel': 'selettur_a916db4e', 'seconds': '초단위', 'log': 'LOG_RECORD', 'at': '현재위치', 'send': 'bagħat', 'main': 'serje', 'req': '요청값', 'hot': 'shortcut_VALUE', 'pump': 'handle_avveniment', 'ROOT': 'pprojetta_għerq', 'marker': '확인표시', 'b': 'SECOND_VALUE', 'command': 'kmand', 'shell': 'shell', 'f': 'fajl_entrata', 'color': '색상', 'click': 'klikkja_buttuna', 'k': '셋째순번', 'c': 'kodiċi_tal_karattru', 'r': '반환값', 'p': 'data_pożizzjoni', 'done': '완료량', 'end': 'ttermina_OFFSET', 'command_mode': 'kmand_MODE', 'key': '누름값', 'y': '세로좌표', 'pixels': '화소들', 'result': 'miżura', 'report': 'validazzjoni_rapport', 'dest': 'destinazzjoni_VALUE_pożizzjoni', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
