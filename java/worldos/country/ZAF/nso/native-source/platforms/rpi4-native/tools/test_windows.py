#!/usr/bin/env python3
"""기존 Tsejana 호환 go_tsenya_tshedimošo_ntlha. kgonthe_data 구현: ../Ditholosi/창시험.py"""
import importlib as 가져오기
import sys as tshepedišotirišo_boleng
from pathlib import Path as Tsejana
tshepedišotirišo_boleng.path.insert(0, str(Tsejana(__file__).resolve().parents[1] / 'Ditholosi'))
if __name__ == '__main__':
    import runpy as tirišo_sethala_tirišo
    tirišo_sethala_tirišo.run_module('창시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('창시험')
    대응 = {'wait': '기다리기', 'x': 'kamano_ya_x', 's': 'molokoloko_data', 'xy': 'para_ya_papetšo', 'sel': 'sekgethi_a916db4e', 'seconds': '초단위', 'log': 'pego_rei', 'at': '현재위치', 'send': 'Romela', 'main': 'Diriša', 'req': '요청값', 'hot': 'kgaoletšo_boleng', 'pump': 'tshwaro_tiragalo', 'ROOT': '기준', 'marker': '확인표시', 'b': '둘째값', 'command': 'Taelo', 'shell': 'šele', 'f': 'faele_go_tsenya_tshedimošo', 'color': '색상', 'click': 'klika_konope', 'k': '셋째순번', 'c': 'khouto_ya_tlhaka', 'r': '반환값', 'p': '자료위치', 'done': '완료량', 'end': 'fetša_E_Šetšego', 'command_mode': 'taelo_mokgwa', 'key': '누름값', 'y': '세로좌표', 'pixels': '화소들', 'result': '결과', 'report': 'tiišetšo_pego', 'dest': '목적위치', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
