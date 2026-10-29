#!/usr/bin/env python3
"""기존 Cale 호환 intrare_p. real_date 구현: ../Instrumente/원격한글시험.py"""
import importlib as TAKE_VALUE
import sys as sistem_de_operare_VALUE
from pathlib import Path as Cale
sistem_de_operare_VALUE.path.insert(0, str(Cale(__file__).resolve().parents[1] / 'Instrumente'))
if __name__ == '__main__':
    import runpy as program_ecrane_de_lansare
    program_ecrane_de_lansare.run_module('원격한글시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('원격한글시험')
    mapare_VALUE = {'wait': '기다리기', 'typing': '글자입력', 'start': 'Pornește', 'profile': 'Profil', 'focused': 'Prioritare', 'serial': '직렬입출력', 'keys': '누름열', 'server': 'server_VALUE', 'log': 'LOG_RECORD', 'args': 'argument_ARRAY', 'deadline': 'dată_limită_oră', 'data': 'date', 'candidate': '후보', 'logs': '기록들', 'kw': 'argument_denumit', 'number': '수치', 'main': 'Pornește', 'ready': '준비완료', 'found': 'căuta_KR', 'guest': 'invitat', 'ROOT': 'Project_rădăcină', 'marker': 'marcaj', 'text': 'SMS', 'out': 'KR_date', 'env': '환경', 'f': 'Fișier_intrare', 'port': 'număr_port', 'offset': 'OFFSET_VALUE', 'version': 'număr_de_versiune', 'p': 'date_poziție', 'selector': 'selector', 'xvfb': '가상표시장치', 'display': 'afișaj', 'n': 'element_COUNT', 'key': '누름값', 'processes': '실행과정들', 'rootfs': '뿌리파일계층', 'xdo': '가상입력도구', 'name': 'Nume', 'window': 'Fereastră', 'report': 'validare_raport', 'work': '작업경로'}
    for Anteriorul_element, curent_element in mapare_VALUE.items():
        if hasattr(구현, curent_element): globals()[Anteriorul_element] = getattr(구현, curent_element)
