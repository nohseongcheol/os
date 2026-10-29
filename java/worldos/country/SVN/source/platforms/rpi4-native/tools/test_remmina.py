#!/usr/bin/env python3
"""기존 POT 호환 vnos_p. dejanski_podatki 구현: ../Orodja/원격한글시험.py"""
import importlib as TAKE_VALUE
import sys as operacijski_sistem_VALUE
from pathlib import Path as POT
operacijski_sistem_VALUE.path.insert(0, str(POT(__file__).resolve().parents[1] / 'Orodja'))
if __name__ == '__main__':
    import runpy as aplikacija_zaganjalnik
    aplikacija_zaganjalnik.run_module('원격한글시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('원격한글시험')
    preslikava_VALUE = {'wait': '기다리기', 'typing': '글자입력', 'start': 'Zaženi', 'profile': 'Profil', 'focused': 'V_fokusu', 'serial': '직렬입출력', 'keys': '누름열', 'server': 'strežnik_VALUE', 'log': 'LOG_zapis', 'args': 'argument_ARRAY', 'deadline': 'rok_čas', 'data': 'podatki', 'candidate': '후보', 'logs': '기록들', 'kw': 'imenovan_argument', 'number': '수치', 'main': 'Zaženi', 'ready': '준비완료', 'found': 'Išči_KR', 'guest': 'gost', 'ROOT': 'pobuda_koren', 'marker': 'oznaka', 'text': 'Besedilo', 'out': 'KR_podatki', 'env': '환경', 'f': 'Datoteka_vnos', 'port': 'številka_vrat', 'offset': 'odmik_VALUE', 'version': 'številka_različice', 'p': 'podatki_položaj', 'selector': 'izbirnik', 'xvfb': 'navidezen_zaslon', 'display': 'zaslon', 'n': 'element_COUNT', 'key': '누름값', 'processes': '실행과정들', 'rootfs': '뿌리파일계층', 'xdo': '가상입력도구', 'name': 'Ime', 'window': 'okno', 'report': 'preverjanje_veljavnosti_prijavi', 'work': '작업경로'}
    for 이전, sprotno_element in preslikava_VALUE.items():
        if hasattr(구현, sprotno_element): globals()[이전] = getattr(구현, sprotno_element)
