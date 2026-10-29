#!/usr/bin/env python3
"""기존 Ýol 호환 girizmeklik_utuk. hakyky_maglumat 구현: ../Gurallar/셸시험.py"""
import importlib as 가져오기
import sys as operasiýa_ulgamy_baha
from pathlib import Path as Ýol
operasiýa_ulgamy_baha.path.insert(0, str(Ýol(__file__).resolve().parents[1] / 'Gurallar'))
if __name__ == '__main__':
    import runpy as programma_programma_paneli
    programma_programma_paneli.run_module('셸시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('셸시험')
    대응 = {'timeout': '시간제한', 'x': 'x_koordinatasy', 'msg': 'Tor_habar', 'i': '순번', 'reply': 'jogap_bermek', 'call': '호출', 'args': 'argument_ARRAY', 'chunk': '조각', 'data': 'maglumat', 'proc': 'Proses', 'long_text': '긴글', 'restored': '복원자료', 'send': 'iber', 'file': 'Faýl', 'main': 'Bitir', 'found': '찾은결과', 'ROOT': '기준', 'text': 'Metin', 'marker': '확인표시', 'command': 'buýruk', 'expected': '예상결과', 'pixel': 'pel', 'shell': 'gabyjak', 'poll': '준비살피미', 'transcript': '대화기록', 'end': 'tamamla_Süýşüriş', 'image': 'surat', 'key': '누름값', 'y': '세로좌표', 'output': '출력결과', 'result': '결과', 'client': 'müşderi', 'line': 'setir', 'stream': 'Stream_baha', 'name': 'Ad', 'value': 'baha', 'receive': '수신하기', 'report': 'barlag_hasabat', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
