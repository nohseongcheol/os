#!/usr/bin/env python3
"""기존 LLWYBR 호환 cofnod_p. go_iawn_data 구현: ../Offer/원격한글시험.py"""
import importlib as TAKE_VALUE
import sys as system_weithredu_VALUE
from pathlib import Path as LLWYBR
system_weithredu_VALUE.path.insert(0, str(LLWYBR(__file__).resolve().parents[1] / 'Offer'))
if __name__ == '__main__':
    import runpy as Rhaglen_lansiwr
    Rhaglen_lansiwr.run_module('원격한글시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('원격한글시험')
    대응 = {'wait': '기다리기', 'typing': '글자입력', 'start': 'Gweithredu_2', 'profile': 'Proffil', 'focused': 'Blaenoriaeth', 'serial': '직렬입출력', 'keys': '누름열', 'server': 'gweinydd_VALUE', 'log': 'LOG_rhes', 'args': 'arg_ARAE', 'deadline': '마감시각', 'data': 'data', 'candidate': '후보', 'logs': '기록들', 'kw': '이름붙인인수', 'number': '수치', 'main': 'Gweithredu_2', 'ready': '준비완료', 'found': 'SEARCH_mesur', 'guest': 'gwestai', 'ROOT': 'prosiect_gwraidd', 'marker': '확인표시', 'text': 'Testun', 'out': 'mesur_data', 'env': '환경', 'f': 'ffeil_cofnod', 'port': 'rhif_porth', 'offset': 'OFFSET_VALUE', 'version': 'rhif_fersiwn', 'p': 'data_safle', 'selector': 'dewisydd', 'xvfb': 'rhith_dangos', 'display': 'dangosydd', 'n': 'eitem_COUNT', 'key': '누름값', 'processes': '실행과정들', 'rootfs': '뿌리파일계층', 'xdo': '가상입력도구', 'name': 'Enw', 'window': 'ffenestr', 'report': 'dilysu_adrodd', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
