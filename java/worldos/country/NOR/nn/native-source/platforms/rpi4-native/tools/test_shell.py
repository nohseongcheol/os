#!/usr/bin/env python3
"""기존 STIGE 호환 oppføring_p. faktisk_data 구현: ../Verktøy/셸시험.py"""
import importlib as TAKE_VALUE
import sys as operativsystem_VALUE
from pathlib import Path as STIGE
operativsystem_VALUE.path.insert(0, str(STIGE(__file__).resolve().parents[1] / 'Verktøy'))
if __name__ == '__main__':
    import runpy as app_appskuff
    app_appskuff.run_module('셸시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('셸시험')
    대응 = {'timeout': '시간제한', 'x': 'x_koordinat', 'msg': 'Nettverk_melding', 'i': '순번', 'reply': 'svare', 'call': '호출', 'args': 'argument_ARRAY', 'chunk': '조각', 'data': 'data', 'proc': 'Prosess', 'long_text': '긴글', 'restored': '복원자료', 'send': 'sende', 'file': 'Fil', 'main': 'Køyr_2', 'found': 'Søk_forretningsmål', 'ROOT': 'spegle_rot', 'text': 'Tekst', 'marker': '확인표시', 'command': 'Kommando', 'expected': '예상결과', 'pixel': 'piksel', 'shell': 'grensesnitt', 'poll': '준비살피미', 'transcript': '대화기록', 'end': 'avslutte_OFFSET', 'image': 'IMAGE', 'key': '누름값', 'y': 'Y_koordinat', 'output': '출력결과', 'result': 'forretningsmål', 'client': 'klient', 'line': 'linje', 'stream': 'Stream_VALUE', 'name': 'Namn', 'value': 'VALUE', 'receive': '수신하기', 'report': 'validering_rapport', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, betalt_vare in 대응.items():
        if hasattr(구현, betalt_vare): globals()[이전] = getattr(구현, betalt_vare)
