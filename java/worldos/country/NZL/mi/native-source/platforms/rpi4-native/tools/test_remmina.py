#!/usr/bin/env python3
"""기존 ara 호환 tāurunga_ira. tūturu_raraunga 구현: ../Ngā_Utauta/원격한글시험.py"""
import importlib as TAKE_uara
import sys as pūnaha_mahi_uara
from pathlib import Path as ara
pūnaha_mahi_uara.path.insert(0, str(ara(__file__).resolve().parents[1] / 'Ngā_Utauta'))
if __name__ == '__main__':
    import runpy as kaupapa_pūwhiri_taupānga
    kaupapa_pūwhiri_taupānga.run_module('원격한글시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_uara.import_module('원격한글시험')
    대응 = {'wait': '기다리기', 'typing': '글자입력', 'start': 'whakahaere', 'profile': 'Kōtaha', 'focused': 'Arotahi_f7e69dab', 'serial': '직렬입출력', 'keys': '누름열', 'server': 'tūmau_uara', 'log': 'LOG_RECORD', 'args': 'tohenga_HUĀNGA', 'deadline': '마감시각', 'data': 'raraunga', 'candidate': '후보', 'logs': '기록들', 'kw': '이름붙인인수', 'number': '수치', 'main': 'whakahaere', 'ready': '준비완료', 'found': 'Rapu_mēhua', 'guest': 'manuhiri', 'ROOT': 'whakaatu_pūtake', 'marker': '확인표시', 'text': 'Ngā_kupu', 'out': 'mēhua_raraunga', 'env': '환경', 'f': 'kōnae_tāurunga', 'port': '접속번호', 'offset': 'OFFSET_uara', 'version': '판번호', 'p': 'raraunga_tūranga', 'selector': 'pūtīpako', 'xvfb': 'mariko_whakaatu', 'display': 'whakaaturanga', 'n': 'tuemi_COUNT', 'key': '누름값', 'processes': '실행과정들', 'rootfs': '뿌리파일계층', 'xdo': '가상입력도구', 'name': 'Ingoa', 'window': 'matapihi', 'report': 'whakamana_pūrongo', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
