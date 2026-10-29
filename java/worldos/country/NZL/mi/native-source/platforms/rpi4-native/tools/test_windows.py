#!/usr/bin/env python3
"""기존 ara 호환 tāurunga_ira. tūturu_raraunga 구현: ../Ngā_Utauta/창시험.py"""
import importlib as TAKE_uara
import sys as pūnaha_mahi_uara
from pathlib import Path as ara
pūnaha_mahi_uara.path.insert(0, str(ara(__file__).resolve().parents[1] / 'Ngā_Utauta'))
if __name__ == '__main__':
    import runpy as kaupapa_pūwhiri_taupānga
    kaupapa_pūwhiri_taupānga.run_module('창시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_uara.import_module('창시험')
    대응 = {'wait': '기다리기', 'x': 'taunga_x', 's': 'aho_raraunga', 'xy': 'takirua_taururuku', 'sel': 'pūtīpako_a916db4e', 'seconds': '초단위', 'log': 'LOG_RECORD', 'at': '현재위치', 'send': 'tuku', 'main': 'whakahaere', 'req': '요청값', 'hot': 'pokatata_uara', 'pump': 'raweke_hui', 'ROOT': 'whakaatu_pūtake', 'marker': '확인표시', 'b': 'SECOND_uara', 'command': 'tono', 'shell': 'anga', 'f': 'kōnae_tāurunga', 'color': '색상', 'click': 'pāwhiri_pātene', 'k': '셋째순번', 'c': 'waehere_pūāhua', 'r': '반환값', 'p': 'raraunga_tūranga', 'done': '완료량', 'end': 'mutu_OFFSET', 'command_mode': 'tono_MODE', 'key': '누름값', 'y': '세로좌표', 'pixels': '화소들', 'result': 'mēhua', 'report': 'whakamana_pūrongo', 'dest': 'ūnga_uara_tūranga', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
