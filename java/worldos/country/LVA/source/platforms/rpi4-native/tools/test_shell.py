#!/usr/bin/env python3
"""기존 CEĻŠ 호환 ieejas_punkts. faktisks_dati 구현: ../Rīki/셸시험.py"""
import importlib as TAKE_VALUE
import sys as operētājsistēma_VALUE
from pathlib import Path as CEĻŠ
operētājsistēma_VALUE.path.insert(0, str(CEĻŠ(__file__).resolve().parents[1] / 'Rīki'))
if __name__ == '__main__':
    import runpy as programma_palaidējs
    programma_palaidējs.run_module('셸시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('셸시험')
    kartēšana_VALUE = {'timeout': '시간제한', 'x': 'x_koordināta', 'msg': 'tīkls_ziņa', 'i': '순번', 'reply': 'atbilde', 'call': '호출', 'args': 'arg_ARRAY', 'chunk': '조각', 'data': 'dati', 'proc': 'Process', 'long_text': '긴글', 'restored': '복원자료', 'send': 'sūtīt', 'file': 'Fails', 'main': 'Palaist', 'found': 'Meklēt_mērs', 'ROOT': 'Project_sakne', 'text': 'Teksts', 'marker': 'marķieris', 'command': 'Komanda', 'expected': '예상결과', 'pixel': 'attēla_elements', 'shell': 'čaula', 'poll': '준비살피미', 'transcript': 'transkripcija', 'end': 'beigt_zvanu_Nobīde', 'image': 'IMAGE', 'key': '누름값', 'y': '세로좌표', 'output': 'ražojums', 'result': 'mērs', 'client': 'klients', 'line': 'Līniju', 'stream': 'Stream_VALUE', 'name': 'Nosaukums', 'value': 'VALUE', 'receive': 'saņemt_ziņa', 'report': 'validācija_ziņot', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, pašreizējais_krājums in kartēšana_VALUE.items():
        if hasattr(구현, pašreizējais_krājums): globals()[이전] = getattr(구현, pašreizējais_krājums)
