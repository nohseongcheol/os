#!/usr/bin/env python3
"""기존 CEĻŠ 호환 ieejas_punkts. faktisks_dati 구현: ../Rīki/창시험.py"""
import importlib as TAKE_VALUE
import sys as operētājsistēma_VALUE
from pathlib import Path as CEĻŠ
operētājsistēma_VALUE.path.insert(0, str(CEĻŠ(__file__).resolve().parents[1] / 'Rīki'))
if __name__ == '__main__':
    import runpy as programma_palaidējs
    programma_palaidējs.run_module('창시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('창시험')
    kartēšana_VALUE = {'wait': '기다리기', 'x': 'x_koordināta', 's': 'virkne_dati', 'xy': 'koordinātu_pāris', 'sel': 'atlasītājs_a916db4e', 'seconds': '초단위', 'log': 'LOG_RECORD', 'at': 'pašreizējais_amats', 'send': 'sūtīt', 'main': 'Palaist', 'req': 'pieprasījums_VALUE', 'hot': 'saīsne_VALUE', 'pump': 'turis_notikums', 'ROOT': 'Project_sakne', 'marker': 'marķieris', 'b': 'SECOND_VALUE', 'command': 'Komanda', 'shell': 'čaula', 'f': 'Fails_ievade', 'color': '색상', 'click': 'klikšķis_poga', 'k': '셋째순번', 'c': 'koda_punkts', 'r': '반환값', 'p': 'dati_amats', 'done': 'Pabeigti_summa', 'end': 'beigt_zvanu_Nobīde', 'command_mode': 'komanda_MODE', 'key': '누름값', 'y': '세로좌표', 'pixels': '화소들', 'result': 'mērs', 'report': 'validācija_ziņot', 'dest': 'mērķis_VALUE_amats', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, pašreizējais_krājums in kartēšana_VALUE.items():
        if hasattr(구현, pašreizējais_krājums): globals()[이전] = getattr(구현, pašreizējais_krājums)
