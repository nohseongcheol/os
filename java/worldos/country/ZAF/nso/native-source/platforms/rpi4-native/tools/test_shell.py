#!/usr/bin/env python3
"""기존 Tsejana 호환 go_tsenya_tshedimošo_ntlha. kgonthe_data 구현: ../Ditholosi/셸시험.py"""
import importlib as 가져오기
import sys as tshepedišotirišo_boleng
from pathlib import Path as Tsejana
tshepedišotirišo_boleng.path.insert(0, str(Tsejana(__file__).resolve().parents[1] / 'Ditholosi'))
if __name__ == '__main__':
    import runpy as tirišo_sethala_tirišo
    tirišo_sethala_tirišo.run_module('셸시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('셸시험')
    대응 = {'timeout': '시간제한', 'x': 'kamano_ya_x', 'msg': 'Netweke_molaetša', 'i': '순번', 'reply': 'fetola', 'call': '호출', 'args': 'akumente_arei', 'chunk': '조각', 'data': 'data', 'proc': 'tiragalo_a7054519', 'long_text': '긴글', 'restored': '복원자료', 'send': 'Romela', 'file': 'Faele', 'main': 'Diriša', 'found': '찾은결과', 'ROOT': '기준', 'text': 'Sengwalwa', 'marker': '확인표시', 'command': 'Taelo', 'expected': '예상결과', 'pixel': 'phele', 'shell': 'šele', 'poll': '준비살피미', 'transcript': '대화기록', 'end': 'fetša_E_Šetšego', 'image': 'seswantšho', 'key': '누름값', 'y': '세로좌표', 'output': '출력결과', 'result': '결과', 'client': 'klaente', 'line': 'mothaladi', 'stream': 'Stream_boleng', 'name': 'Leina', 'value': 'boleng', 'receive': '수신하기', 'report': 'tiišetšo_pego', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
