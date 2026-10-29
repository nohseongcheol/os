#!/usr/bin/env python3
"""기존 Pad 호환 inskrywing_p. werklik_data 구현: ../Nutsmiddels/화면요소시험.py"""
import importlib as TAKE_VALUE
import sys as bedryfstelsel_VALUE
from pathlib import Path as Pad
bedryfstelsel_VALUE.path.insert(0, str(Pad(__file__).resolve().parents[1] / 'Nutsmiddels'))
if __name__ == '__main__':
    import runpy as program_oopmaker
    program_oopmaker.run_module('화면요소시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('화면요소시험')
    대응 = {'wait': '기다리기', 'x': 'x_koördinaat', 's': 'string_data', 'i': '순번', 'sel': 'selekteerder_a916db4e', 'seconds': '초단위', 'log': 'LOG_ry', 'data': 'data', 'at': '현재위치', 'send': 'e_pos', 'main': 'Loop', 'req': '요청값', 'hot': 'kortpad_VALUE', 'pump': 'handvatsel_gebeurtenis', 'ROOT': 'Project_wortel', 'marker': '확인표시', 'b': 'SECOND_VALUE', 'command': 'Opdrag', 'shell': 'dop', 'f': 'lêer_inskrywing', 'click': 'klik_knoppie', 'k': '셋째순번', 'c': 'karakterkode', 'r': '반환값', 'p': 'data_plaas', 'command_mode': 'bevel_MODE', 'end': 'beëindig_OFFSET', 'classes': 'Klas_pad', 'key': '누름값', 'y': 'Y_koördinaat', 'result': 'maatreël', 'report': 'validering_verslag', 'dest': 'bestemming_VALUE_plaas', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
