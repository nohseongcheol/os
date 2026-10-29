#!/usr/bin/env python3
"""기존 ara 호환 tāurunga_ira. tūturu_raraunga 구현: ../Ngā_Utauta/셸시험.py"""
import importlib as TAKE_uara
import sys as pūnaha_mahi_uara
from pathlib import Path as ara
pūnaha_mahi_uara.path.insert(0, str(ara(__file__).resolve().parents[1] / 'Ngā_Utauta'))
if __name__ == '__main__':
    import runpy as kaupapa_pūwhiri_taupānga
    kaupapa_pūwhiri_taupānga.run_module('셸시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_uara.import_module('셸시험')
    대응 = {'timeout': '시간제한', 'x': 'taunga_x', 'msg': 'whatunga_karere', 'i': '순번', 'reply': 'whakautu', 'call': '호출', 'args': 'tohenga_HUĀNGA', 'chunk': '조각', 'data': 'raraunga', 'proc': 'Hātepe', 'long_text': '긴글', 'restored': '복원자료', 'send': 'tuku', 'file': 'Kōnae', 'main': 'whakahaere', 'found': 'Rapu_mēhua', 'ROOT': 'whakaatu_pūtake', 'text': 'Ngā_kupu', 'marker': '확인표시', 'command': 'tono', 'expected': '예상결과', 'pixel': 'pika', 'shell': 'anga', 'poll': '준비살피미', 'transcript': '대화기록', 'end': 'mutu_OFFSET', 'image': 'IMAGE', 'key': '누름값', 'y': '세로좌표', 'output': '출력결과', 'result': 'mēhua', 'client': 'kiritaki', 'line': 'hononga', 'stream': 'roma_uara', 'name': 'Ingoa', 'value': 'uara', 'receive': '수신하기', 'report': 'whakamana_pūrongo', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
