#!/usr/bin/env python3
"""기존 LLWYBR 호환 cofnod_p. go_iawn_data 구현: ../Offer/창시험.py"""
import importlib as TAKE_VALUE
import sys as system_weithredu_VALUE
from pathlib import Path as LLWYBR
system_weithredu_VALUE.path.insert(0, str(LLWYBR(__file__).resolve().parents[1] / 'Offer'))
if __name__ == '__main__':
    import runpy as Rhaglen_lansiwr
    Rhaglen_lansiwr.run_module('창시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('창시험')
    대응 = {'wait': '기다리기', 'x': 'cyfesuryn_x', 's': 'testun_data', 'xy': 'pâr_o_gyfesurynnau', 'sel': 'dewisydd_a916db4e', 'seconds': '초단위', 'log': 'LOG_rhes', 'at': '현재위치', 'send': 'anfon', 'main': 'Gweithredu_2', 'req': 'cais_HTTP_VALUE', 'hot': 'llwybr_byr_VALUE', 'pump': 'dolen_digwyddiad', 'ROOT': 'prosiect_gwraidd', 'marker': '확인표시', 'b': 'SECOND_VALUE', 'command': 'Gorchymyn', 'shell': 'cragen', 'f': 'ffeil_cofnod', 'color': '색상', 'click': 'clicio_botwm', 'k': '셋째순번', 'c': 'cod_nod', 'r': '반환값', 'p': 'data_safle', 'done': '완료량', 'end': 'gorffen_OFFSET', 'command_mode': 'gorchymyn_MODE', 'key': '누름값', 'y': 'Y_cyfesuryn', 'pixels': '화소들', 'result': 'mesur', 'report': 'dilysu_adrodd', 'dest': 'cyrchfan_VALUE_safle', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
