#!/usr/bin/env python3
"""기존 Inzira 호환 icyinjizwa_inota. nyakuri_amakurushingiro 구현: ../Ibikoresho/셸시험.py"""
import importlib as 가져오기
import sys as sisitemu_ngengamikorere_agaciro
from pathlib import Path as Inzira
sisitemu_ngengamikorere_agaciro.path.insert(0, str(Inzira(__file__).resolve().parents[1] / 'Ibikoresho'))
if __name__ == '__main__':
    import runpy as porogaramu_umukozi
    porogaramu_umukozi.run_module('셸시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('셸시험')
    대응 = {'timeout': '시간제한', 'x': 'Ihuza_rya_x', 'msg': 'Urusobemiyoboro_ubutumwa', 'i': '순번', 'reply': 'gusubiza', 'call': '호출', 'args': 'ingingo_ARRAY', 'chunk': '조각', 'data': 'amakurushingiro', 'proc': 'Inzira_a7054519', 'long_text': '긴글', 'restored': '복원자료', 'send': 'kohereza', 'file': 'Idosiye', 'main': 'ihuriro', 'found': '찾은결과', 'ROOT': '기준', 'text': 'Umwandiko', 'marker': '확인표시', 'command': 'Icyo_wifuza', 'expected': '예상결과', 'pixel': 'pel', 'shell': 'insomamabwiriza', 'poll': '준비살피미', 'transcript': '대화기록', 'end': 'kurangiza_Ofuseti', 'image': 'ishusho', 'key': '누름값', 'y': '세로좌표', 'output': '출력결과', 'result': '결과', 'client': 'umukiriya', 'line': 'umurongo', 'stream': 'Stream_agaciro', 'name': 'Izina', 'value': 'agaciro', 'receive': '수신하기', 'report': 'iyemeza_raporo', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
