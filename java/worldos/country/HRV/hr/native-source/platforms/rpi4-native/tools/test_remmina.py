#!/usr/bin/env python3
"""기존 PUTANJA 호환 unos_p. stvaran_podaci 구현: ../Alati/원격한글시험.py"""
import importlib as TAKE_VALUE
import sys as operacijski_sustav_VALUE
from pathlib import Path as PUTANJA
operacijski_sustav_VALUE.path.insert(0, str(PUTANJA(__file__).resolve().parents[1] / 'Alati'))
if __name__ == '__main__':
    import runpy as program_pokretač
    program_pokretač.run_module('원격한글시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('원격한글시험')
    mapiranje_VALUE = {'wait': '기다리기', 'typing': '글자입력', 'start': 'Pokreni', 'profile': 'Profil', 'focused': 'U_fokusu', 'serial': '직렬입출력', 'keys': '누름열', 'server': 'server_VALUE', 'log': 'LOG_zapis', 'args': 'argument_ARRAY', 'deadline': 'rok_za_dovršetak_TIME', 'data': 'podaci', 'candidate': '후보', 'logs': '기록들', 'kw': 'imenovani_argument', 'number': '수치', 'main': 'Pokreni', 'ready': '준비완료', 'found': 'Traži_KR', 'guest': 'gost', 'ROOT': 'akcija_korijen', 'marker': 'marker', 'text': 'Tekst', 'out': 'KR_podaci', 'env': 'okruženje', 'f': 'Datoteka_unos', 'port': 'broj_priključka', 'offset': 'pomak_VALUE', 'version': 'broj_verzije', 'p': 'podaci_položaj', 'selector': 'odabirač', 'xvfb': '가상표시장치', 'display': 'zaslon', 'n': 'artikl_COUNT', 'key': '누름값', 'processes': '실행과정들', 'rootfs': '뿌리파일계층', 'xdo': '가상입력도구', 'name': 'Ime', 'window': 'Prozor', 'report': 'provjera_izvješće', 'work': '작업경로'}
    for 이전, redovno_artikl in mapiranje_VALUE.items():
        if hasattr(구현, redovno_artikl): globals()[이전] = getattr(구현, redovno_artikl)
