#!/usr/bin/env python3
"""기존 njia 호환 ingizo_pointi. halisi_data 구현: ../Zana/셸시험.py"""
import importlib as 가져오기
import sys as mfumo_endeshi_thamani
from pathlib import Path as njia
mfumo_endeshi_thamani.path.insert(0, str(njia(__file__).resolve().parents[1] / 'Zana'))
if __name__ == '__main__':
    import runpy as programu_droo_ya_programu
    programu_droo_ya_programu.run_module('셸시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('셸시험')
    대응 = {'timeout': '시간제한', 'x': 'jira_x', 'msg': 'Mtandao_ujumbe', 'i': '순번', 'reply': 'jibu', 'call': '호출', 'args': 'hoja_ARRAY', 'chunk': '조각', 'data': 'data', 'proc': 'Mchakato', 'long_text': '긴글', 'restored': '복원자료', 'send': 'tuma', 'file': 'faili', 'main': 'endesha', 'found': '찾은결과', 'ROOT': '기준', 'text': 'SMS', 'marker': '확인표시', 'command': 'amri', 'expected': '예상결과', 'pixel': 'elepi', 'shell': 'sheli', 'poll': '준비살피미', 'transcript': '대화기록', 'end': 'tamatia_Chipua', 'image': 'picha', 'key': '누름값', 'y': 'Kitufe_cha_Y_kiratibu', 'output': '출력결과', 'result': '결과', 'client': 'teja', 'line': 'laini', 'stream': 'Stream_thamani', 'name': 'Jina', 'value': 'thamani', 'receive': '수신하기', 'report': 'uhakikishi_ripoti', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
