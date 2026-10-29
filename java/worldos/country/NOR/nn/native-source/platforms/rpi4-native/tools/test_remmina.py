#!/usr/bin/env python3
"""기존 STIGE 호환 oppføring_p. faktisk_data 구현: ../Verktøy/원격한글시험.py"""
import importlib as TAKE_VALUE
import sys as operativsystem_VALUE
from pathlib import Path as STIGE
operativsystem_VALUE.path.insert(0, str(STIGE(__file__).resolve().parents[1] / 'Verktøy'))
if __name__ == '__main__':
    import runpy as app_appskuff
    app_appskuff.run_module('원격한글시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('원격한글시험')
    대응 = {'wait': '기다리기', 'typing': '글자입력', 'start': 'Køyr_2', 'profile': 'Profil', 'focused': 'Fokus_f7e69dab', 'serial': '직렬입출력', 'keys': '누름열', 'server': 'tenar_VALUE', 'log': 'LOG_rad', 'args': 'argument_ARRAY', 'deadline': '마감시각', 'data': 'data', 'candidate': '후보', 'logs': '기록들', 'kw': 'namngitt_argument', 'number': '수치', 'main': 'Køyr_2', 'ready': '준비완료', 'found': 'Søk_forretningsmål', 'guest': 'gjest', 'ROOT': 'spegle_rot', 'marker': '확인표시', 'text': 'Tekst', 'out': 'forretningsmål_data', 'env': '환경', 'f': 'fil_oppføring', 'port': 'portnummer', 'offset': 'OFFSET_VALUE', 'version': '판번호', 'p': 'data_plassere', 'selector': 'veljar', 'xvfb': 'virtuell_vise', 'display': 'skjerm', 'n': 'vare_COUNT', 'key': '누름값', 'processes': '실행과정들', 'rootfs': '뿌리파일계층', 'xdo': '가상입력도구', 'name': 'Namn', 'window': 'vindauge', 'report': 'validering_rapport', 'work': '작업경로'}
    for 이전, betalt_vare in 대응.items():
        if hasattr(구현, betalt_vare): globals()[이전] = getattr(구현, betalt_vare)
