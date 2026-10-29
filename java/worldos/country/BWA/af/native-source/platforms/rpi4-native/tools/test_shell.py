#!/usr/bin/env python3
"""기존 Pad 호환 inskrywing_p. werklik_data 구현: ../Nutsmiddels/셸시험.py"""
import importlib as TAKE_VALUE
import sys as bedryfstelsel_VALUE
from pathlib import Path as Pad
bedryfstelsel_VALUE.path.insert(0, str(Pad(__file__).resolve().parents[1] / 'Nutsmiddels'))
if __name__ == '__main__':
    import runpy as program_oopmaker
    program_oopmaker.run_module('셸시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('셸시험')
    대응 = {'timeout': '시간제한', 'x': 'x_koördinaat', 'msg': 'Netwerk_e_pos', 'i': '순번', 'reply': 'antwoord', 'call': '호출', 'args': 'argument_ARRAY', 'chunk': '조각', 'data': 'data', 'proc': 'Proses', 'long_text': '긴글', 'restored': '복원자료', 'send': 'e_pos', 'file': 'Lêer', 'main': 'Loop', 'found': 'Soek_maatreël', 'ROOT': 'Project_wortel', 'text': 'Teks', 'marker': '확인표시', 'command': 'Opdrag', 'expected': '예상결과', 'pixel': 'pieksel', 'shell': 'dop', 'poll': '준비살피미', 'transcript': '대화기록', 'end': 'beëindig_OFFSET', 'image': 'foto', 'key': '누름값', 'y': 'Y_koördinaat', 'output': '출력결과', 'result': 'maatreël', 'client': 'kliënt', 'line': 'lyn', 'stream': 'Stream_VALUE', 'name': 'Naam', 'value': 'VALUE', 'receive': '수신하기', 'report': 'validering_verslag', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
