#!/usr/bin/env python3
"""기존 Wee 호환 Agab_Punkt. aktuell_Daten 구현: ../Tools/셸시험.py"""
import importlib as TAKE_VALUE
import sys as Betribssystem_VALUE
from pathlib import Path as Wee
Betribssystem_VALUE.path.insert(0, str(Wee(__file__).resolve().parents[1] / 'Tools'))
if __name__ == '__main__':
    import runpy as App_App_Beräich
    App_App_Beräich.run_module('셸시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('셸시험')
    대응 = {'timeout': '시간제한', 'x': 'X_Koordinat', 'msg': 'Reseau_Noriicht', 'i': '순번', 'reply': 'äntweren', 'call': '호출', 'args': 'Argument_ARRAY', 'chunk': '조각', 'data': 'Daten', 'proc': 'Prozess', 'long_text': '긴글', 'restored': '복원자료', 'send': 'mailen', 'file': 'Fichier', 'main': 'Laf', 'found': 'Sich_Mooss', 'ROOT': 'projezéieren_Racinn', 'text': 'SMS', 'marker': 'Markéierung', 'command': 'Befeel', 'expected': '예상결과', 'pixel': 'Pel', 'shell': 'Shell', 'poll': '준비살피미', 'transcript': '대화기록', 'end': 'bëennegen_OFFSET', 'image': 'Bild', 'key': '누름값', 'y': '세로좌표', 'output': '출력결과', 'result': 'Mooss', 'client': 'Client', 'line': 'Zeil', 'stream': 'Stream_VALUE', 'name': 'Numm', 'value': 'VALUE', 'receive': '수신하기', 'report': 'Validatioun_mellen', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
