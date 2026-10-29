#!/usr/bin/env python3
"""기존 mogħdija 호환 entrata_punt. attwali_data 구현: ../Għodod/원격한글시험.py"""
import importlib as TAKE_VALUE
import sys as sistema_operattiva_VALUE
from pathlib import Path as mogħdija
sistema_operattiva_VALUE.path.insert(0, str(mogħdija(__file__).resolve().parents[1] / 'Għodod'))
if __name__ == '__main__':
    import runpy as programm_ġabra_ta_apps
    programm_ġabra_ta_apps.run_module('원격한글시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('원격한글시험')
    대응 = {'wait': '기다리기', 'typing': '글자입력', 'start': 'serje', 'profile': 'Profil', 'focused': 'Ffokata', 'serial': '직렬입출력', 'keys': '누름열', 'server': 'server_VALUE', 'log': 'LOG_RECORD', 'args': 'argument_ARRAY', 'deadline': '마감시각', 'data': 'data', 'candidate': '후보', 'logs': '기록들', 'kw': '이름붙인인수', 'number': '수치', 'main': 'serje', 'ready': '준비완료', 'found': 'SEARCH_miżura', 'guest': 'mistieden', 'ROOT': 'pprojetta_għerq', 'marker': '확인표시', 'text': 'SMS', 'out': 'miżura_data', 'env': '환경', 'f': 'fajl_entrata', 'port': '접속번호', 'offset': 'OFFSET_VALUE', 'version': '판번호', 'p': 'data_pożizzjoni', 'selector': 'selettur', 'xvfb': 'virtwali_wera', 'display': 'displej', 'n': 'element_COUNT', 'key': '누름값', 'processes': '실행과정들', 'rootfs': '뿌리파일계층', 'xdo': '가상입력도구', 'name': 'isem', 'window': 'tieqa', 'report': 'validazzjoni_rapport', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
