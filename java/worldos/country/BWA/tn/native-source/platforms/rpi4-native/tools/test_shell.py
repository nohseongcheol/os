#!/usr/bin/env python3
"""기존 tsela 호환 tsenyo_ntlha. tota_tshedimosetso 구현: ../Thuluse/셸시험.py"""
import importlib as 가져오기
import sys as Tsamaisotiriso_Boleng
from pathlib import Path as tsela
Tsamaisotiriso_Boleng.path.insert(0, str(tsela(__file__).resolve().parents[1] / 'Thuluse'))
if __name__ == '__main__':
    import runpy as Tiriso_llae_ya_sediriso
    Tiriso_llae_ya_sediriso.run_module('셸시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('셸시험')
    대응 = {'timeout': '시간제한', 'x': 'kgokagano_ya_x', 'msg': 'Neteweke_molaetsa', 'i': '순번', 'reply': 'araba', 'call': '호출', 'args': 'Thulaganyo_setlhopha', 'chunk': '조각', 'data': 'tshedimosetso', 'proc': 'Thulaganyo', 'long_text': '긴글', 'restored': '복원자료', 'send': 'romela', 'file': 'faele', 'main': 'dirisa', 'found': '찾은결과', 'ROOT': '기준', 'text': 'SMS', 'marker': '확인표시', 'command': 'Taelo', 'expected': '예상결과', 'pixel': 'phele', 'shell': 'setlhalosataelo', 'poll': '준비살피미', 'transcript': '대화기록', 'end': 'kgaola_Baya_ka_Tekatekanyo', 'image': 'Setshwantsho', 'key': '누름값', 'y': '세로좌표', 'output': '출력결과', 'result': '결과', 'client': 'sedirelwa', 'line': 'Mola', 'stream': 'moela_Boleng', 'name': 'leina', 'value': 'Boleng', 'receive': '수신하기', 'report': 'netefatso_pego', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, ga_jaana_selwana in 대응.items():
        if hasattr(구현, ga_jaana_selwana): globals()[이전] = getattr(구현, ga_jaana_selwana)
