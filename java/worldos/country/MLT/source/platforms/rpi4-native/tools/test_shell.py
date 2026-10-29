#!/usr/bin/env python3
"""기존 mogħdija 호환 entrata_punt. attwali_data 구현: ../Għodod/셸시험.py"""
import importlib as TAKE_VALUE
import sys as sistema_operattiva_VALUE
from pathlib import Path as mogħdija
sistema_operattiva_VALUE.path.insert(0, str(mogħdija(__file__).resolve().parents[1] / 'Għodod'))
if __name__ == '__main__':
    import runpy as programm_ġabra_ta_apps
    programm_ġabra_ta_apps.run_module('셸시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('셸시험')
    대응 = {'timeout': '시간제한', 'x': 'koordinat_x', 'msg': 'netwerk_messaġġ', 'i': '순번', 'reply': 'wieġeb', 'call': '호출', 'args': 'argument_ARRAY', 'chunk': '조각', 'data': 'data', 'proc': 'Proċess', 'long_text': '긴글', 'restored': '복원자료', 'send': 'bagħat', 'file': 'fajl', 'main': 'serje', 'found': 'SEARCH_miżura', 'ROOT': 'pprojetta_għerq', 'text': 'SMS', 'marker': '확인표시', 'command': 'kmand', 'expected': '예상결과', 'pixel': 'pel', 'shell': 'shell', 'poll': '준비살피미', 'transcript': '대화기록', 'end': 'ttermina_OFFSET', 'image': 'IMAGE', 'key': '누름값', 'y': '세로좌표', 'output': '출력결과', 'result': 'miżura', 'client': 'klijent', 'line': 'linja', 'stream': 'Stream_VALUE', 'name': 'isem', 'value': 'VALUE', 'receive': '수신하기', 'report': 'validazzjoni_rapport', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
