#!/usr/bin/env python3
"""기존 Slighe 호환 cur_a_steach_puing. dearbh_dàta 구현: ../innealan/셸시험.py"""
import importlib as TAKE_VALUE
import sys as siostam_obrachaidh_VALUE
from pathlib import Path as Slighe
siostam_obrachaidh_VALUE.path.insert(0, str(Slighe(__file__).resolve().parents[1] / 'innealan'))
if __name__ == '__main__':
    import runpy as ap_drathair_nan_aplacaid
    ap_drathair_nan_aplacaid.run_module('셸시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('셸시험')
    대응 = {'timeout': '시간제한', 'x': 'co_chomharra_x', 'msg': 'lìonra_teachdaireachd', 'i': '순번', 'reply': 'freagair', 'call': '호출', 'args': 'argamaid_ARRAY', 'chunk': '조각', 'data': 'dàta', 'proc': 'Pròiseas', 'long_text': '긴글', 'restored': '복원자료', 'send': 'cuir', 'file': 'faidhle', 'main': 'ruith', 'found': 'lorg_tomhas', 'ROOT': 'tilg_freumh', 'text': 'SMS', 'marker': '확인표시', 'command': 'àithne', 'expected': '예상결과', 'pixel': 'pel', 'shell': 'slige', 'poll': '준비살피미', 'transcript': '대화기록', 'end': 'crìochnaich_OFFSET', 'image': 'IMAGE', 'key': '누름값', 'y': '세로좌표', 'output': '출력결과', 'result': 'tomhas', 'client': 'cliant', 'line': 'loidhne', 'stream': 'sruth_VALUE', 'name': 'Ainm', 'value': 'VALUE', 'receive': '수신하기', 'report': 'dearbhadh_aithisg', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
