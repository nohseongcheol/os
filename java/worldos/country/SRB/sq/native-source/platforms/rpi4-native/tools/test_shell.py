#!/usr/bin/env python3
"""기존 POZICIONI 호환 futje_p. aktual_të_dhëna 구현: ../Mjete/셸시험.py"""
import importlib as TAKE_VALUE
import sys as sistem_operativ_VALUE
from pathlib import Path as POZICIONI
sistem_operativ_VALUE.path.insert(0, str(POZICIONI(__file__).resolve().parents[1] / 'Mjete'))
if __name__ == '__main__':
    import runpy as program_hapës
    program_hapës.run_module('셸시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('셸시험')
    대응 = {'timeout': '시간제한', 'x': 'koordinata_x', 'msg': 'rrjet_email', 'i': '순번', 'reply': 'replikë', 'call': '호출', 'args': 'argument_ARRAY', 'chunk': '조각', 'data': 'të_dhëna', 'proc': 'Proçes', 'long_text': '긴글', 'restored': '복원자료', 'send': 'dërgoj', 'file': 'Kartelë', 'main': 'Ekzekuto', 'found': 'Kërkim_llogaritje', 'ROOT': 'Project_rrënjë', 'text': 'Teksti', 'marker': '확인표시', 'command': 'Komanda', 'expected': '예상결과', 'pixel': 'pikëz', 'shell': 'pasues', 'poll': '준비살피미', 'transcript': '대화기록', 'end': 'mbaroj_OFFSET', 'image': 'IMAGE', 'key': '누름값', 'y': 'Y_koordinatë', 'output': '출력결과', 'result': 'llogaritje', 'client': 'klient', 'line': 'linjë', 'stream': 'Stream_VALUE', 'name': 'Emër', 'value': 'VALUE', 'receive': '수신하기', 'report': 'miratim_raport', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
