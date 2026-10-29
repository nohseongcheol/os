#!/usr/bin/env python3
"""기존 SLÓÐ 호환 færsla_P. raun_gögn 구현: ../Verkfæri/원격한글시험.py"""
import importlib as TAKE_VALUE
import sys as stýrikerfi_VALUE
from pathlib import Path as SLÓÐ
stýrikerfi_VALUE.path.insert(0, str(SLÓÐ(__file__).resolve().parents[1] / 'Verkfæri'))
if __name__ == '__main__':
    import runpy as forrit_ræsir
    forrit_ræsir.run_module('원격한글시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('원격한글시험')
    vörpun_VALUE = {'wait': '기다리기', 'typing': '글자입력', 'start': 'Keyra_2', 'profile': 'prófíll', 'focused': 'Forgangur', 'serial': '직렬입출력', 'keys': '누름열', 'server': 'þjónn_VALUE', 'log': 'LOG_lína', 'args': 'frumbreyta_ARRAY', 'deadline': '마감시각', 'data': 'gögn', 'candidate': '후보', 'logs': '기록들', 'kw': '이름붙인인수', 'number': '수치', 'main': 'Keyra_2', 'ready': '준비완료', 'found': 'Leit_mæld_stærð', 'guest': 'gestur', 'ROOT': 'verk_rót', 'marker': '확인표시', 'text': 'Texti', 'out': 'mæld_stærð_gögn', 'env': '환경', 'f': 'skrá_færsla_3d0c1245', 'port': 'tengisnúmer', 'offset': 'OFFSET_VALUE', 'version': 'útgáfa_númer', 'p': 'gögn_staða', 'selector': 'val', 'xvfb': 'sýndar_birta', 'display': 'skjár', 'n': 'vara_COUNT', 'key': '누름값', 'processes': '실행과정들', 'rootfs': '뿌리파일계층', 'xdo': '가상입력도구', 'name': 'Heiti', 'window': 'Gluggi', 'report': 'prófun_skrá', 'work': '작업경로'}
    for 이전, 현재 in vörpun_VALUE.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
