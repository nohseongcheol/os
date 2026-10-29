#!/usr/bin/env python3
"""기존 Putanja 호환 unos_p. stvaran_podaci 구현: ../Alati/원격한글시험.py"""
import importlib as TAKE_VALUE
import sys as operativni_sistem_VALUE
from pathlib import Path as Putanja
operativni_sistem_VALUE.path.insert(0, str(Putanja(__file__).resolve().parents[1] / 'Alati'))
if __name__ == '__main__':
    import runpy as program_pokretač
    program_pokretač.run_module('원격한글시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('원격한글시험')
    대응 = {'wait': '기다리기', 'typing': '글자입력', 'start': 'Pokreni', 'profile': 'Profil', 'focused': 'U_fokusu', 'serial': '직렬입출력', 'keys': '누름열', 'server': 'server_VALUE', 'log': 'LOG_red', 'args': 'argument_niz', 'deadline': '마감시각', 'data': 'podaci', 'candidate': '후보', 'logs': '기록들', 'kw': '이름붙인인수', 'number': '수치', 'main': 'Pokreni', 'ready': '준비완료', 'found': 'Traži_mjera', 'guest': 'gost', 'ROOT': 'projicirati_koijen', 'marker': '확인표시', 'text': 'Tekst', 'out': 'mjera_podaci', 'env': 'operativno_okruženje', 'f': 'fajl_unos', 'port': 'broj_priključka', 'offset': 'Pomak_VALUE', 'version': 'broj_verzije', 'p': 'podaci_položaj', 'selector': 'birač', 'xvfb': 'virtualno_ekran', 'display': 'ekran', 'n': 'stavka_COUNT', 'key': '누름값', 'processes': '실행과정들', 'rootfs': '뿌리파일계층', 'xdo': '가상입력도구', 'name': 'Naziv', 'window': 'prozor', 'report': 'provjera_izvještaj', 'work': '작업경로'}
    for 이전, trenutno_stavka in 대응.items():
        if hasattr(구현, trenutno_stavka): globals()[이전] = getattr(구현, trenutno_stavka)
