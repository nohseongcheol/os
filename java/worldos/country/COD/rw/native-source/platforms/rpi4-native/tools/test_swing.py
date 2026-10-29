#!/usr/bin/env python3
"""기존 Inzira 호환 icyinjizwa_inota. nyakuri_amakurushingiro 구현: ../Ibikoresho/화면요소시험.py"""
import importlib as 가져오기
import sys as sisitemu_ngengamikorere_agaciro
from pathlib import Path as Inzira
sisitemu_ngengamikorere_agaciro.path.insert(0, str(Inzira(__file__).resolve().parents[1] / 'Ibikoresho'))
if __name__ == '__main__':
    import runpy as porogaramu_umukozi
    porogaramu_umukozi.run_module('화면요소시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('화면요소시험')
    대응 = {'wait': '기다리기', 'x': 'Ihuza_rya_x', 's': 'igicenteruro_amakurushingiro', 'i': '순번', 'sel': 'muhitamo_a916db4e', 'seconds': '초단위', 'log': 'kubika_umurongo', 'data': 'amakurushingiro', 'at': '현재위치', 'send': 'kohereza', 'main': 'ihuriro', 'req': '요청값', 'hot': 'ihinanzira_agaciro', 'pump': 'umukondo_icyabaye', 'ROOT': '기준', 'marker': '확인표시', 'b': '둘째값', 'command': 'Icyo_wifuza', 'shell': 'insomamabwiriza', 'f': 'dosiye_icyinjizwa', 'click': 'gukanda_buto', 'k': '셋째순번', 'c': '문자값', 'r': '반환값', 'p': '자료위치', 'command_mode': 'ibwiriza_uburyo', 'end': 'kurangiza_Ofuseti', 'classes': 'icyiciro_inzira', 'key': '누름값', 'y': '세로좌표', 'result': '결과', 'report': 'iyemeza_raporo', 'dest': '목적위치', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
