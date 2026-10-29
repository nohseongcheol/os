#!/usr/bin/env python3
"""기존 putanja 호환 stavka_p. stvarni_podaci 구현: ../Alatke/원격한글시험.py"""
import importlib as TAKE_VALUE
import sys as operativni_sistem_VALUE
from pathlib import Path as putanja
operativni_sistem_VALUE.path.insert(0, str(putanja(__file__).resolve().parents[1] / 'Alatke'))
if __name__ == '__main__':
    import runpy as program_pokretač
    program_pokretač.run_module('원격한글시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('원격한글시험')
    mapiranje_VALUE = {'wait': '기다리기', 'typing': '글자입력', 'start': 'koristiti', 'profile': 'Profil', 'focused': 'U_fokusu', 'serial': '직렬입출력', 'keys': '누름열', 'server': 'server_VALUE', 'log': 'LOG_snimi', 'args': 'argument_niz', 'deadline': 'krajnji_rok_TIME', 'data': 'podaci', 'candidate': '후보', 'logs': '기록들', 'kw': 'imenovani_argument', 'number': '수치', 'main': 'koristiti', 'ready': '준비완료', 'found': 'SEARCH_KR', 'guest': 'gost', 'ROOT': 'radnja_koren', 'marker': 'označivač', 'text': 'SMS', 'out': 'KR_podaci', 'env': '환경', 'f': 'Datoteka_stavka', 'port': 'broj_porta', 'offset': 'Pomak_VALUE', 'version': 'broj_verzije', 'p': 'podaci_pozicija', 'selector': 'birač', 'xvfb': '가상표시장치', 'display': 'ekran', 'n': 'stavka_COUNT', 'key': '누름값', 'processes': '실행과정들', 'rootfs': '뿌리파일계층', 'xdo': '가상입력도구', 'name': 'ime', 'window': 'prozor', 'report': 'provera_valjanosti_izveštaj', 'work': '작업경로'}
    for 이전, aktuelno_stavka in mapiranje_VALUE.items():
        if hasattr(구현, aktuelno_stavka): globals()[이전] = getattr(구현, aktuelno_stavka)
