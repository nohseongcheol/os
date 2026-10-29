#!/usr/bin/env python3
"""기존 Pad 호환 inskrywing_p. werklik_data 구현: ../Nutsmiddels/원격한글시험.py"""
import importlib as TAKE_VALUE
import sys as bedryfstelsel_VALUE
from pathlib import Path as Pad
bedryfstelsel_VALUE.path.insert(0, str(Pad(__file__).resolve().parents[1] / 'Nutsmiddels'))
if __name__ == '__main__':
    import runpy as program_oopmaker
    program_oopmaker.run_module('원격한글시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('원격한글시험')
    대응 = {'wait': '기다리기', 'typing': '글자입력', 'start': 'Loop', 'profile': 'Profiel', 'focused': 'Gefokus', 'serial': '직렬입출력', 'keys': '누름열', 'server': 'bediener_VALUE', 'log': 'LOG_ry', 'args': 'argument_ARRAY', 'deadline': '마감시각', 'data': 'data', 'candidate': '후보', 'logs': '기록들', 'kw': '이름붙인인수', 'number': '수치', 'main': 'Loop', 'ready': '준비완료', 'found': 'Soek_maatreël', 'guest': 'gas', 'ROOT': 'Project_wortel', 'marker': '확인표시', 'text': 'Teks', 'out': 'maatreël_data', 'env': '환경', 'f': 'lêer_inskrywing', 'port': '접속번호', 'offset': 'OFFSET_VALUE', 'version': '판번호', 'p': 'data_plaas', 'selector': 'selekteerder', 'xvfb': 'virtueel_wys', 'display': 'skerm', 'n': 'item_COUNT', 'key': '누름값', 'processes': '실행과정들', 'rootfs': '뿌리파일계층', 'xdo': '가상입력도구', 'name': 'Naam', 'window': 'venster', 'report': 'validering_verslag', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
