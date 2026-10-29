#!/usr/bin/env python3
"""기존 Cesta 호환 položka_bod. skutočný_údaje 구현: ../Nástroje/원격한글시험.py"""
import importlib as TAKE_VALUE
import sys as operačný_systém_VALUE
from pathlib import Path as Cesta
operačný_systém_VALUE.path.insert(0, str(Cesta(__file__).resolve().parents[1] / 'Nástroje'))
if __name__ == '__main__':
    import runpy as program_spúšťač
    program_spúšťač.run_module('원격한글시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('원격한글시험')
    mapovanie_VALUE = {'wait': '기다리기', 'typing': '글자입력', 'start': 'Spustiť_2', 'profile': 'Profil', 'focused': 'Prioritné', 'serial': '직렬입출력', 'keys': '누름열', 'server': 'server_VALUE', 'log': 'LOG_RECORD', 'args': 'argument_pole', 'deadline': 'termín_čas', 'data': 'údaje', 'candidate': '후보', 'logs': '기록들', 'kw': 'pomenované_argumenty', 'number': '수치', 'main': 'Spustiť_2', 'ready': '준비완료', 'found': 'Hľadať_KR', 'guest': 'hosť', 'ROOT': 'akcia_koreň', 'marker': 'fixka', 'text': 'Spracovanie_textu', 'out': 'KR_údaje', 'env': '환경', 'f': 'Súbor_položka', 'port': 'číslo_portu', 'offset': 'Posun_VALUE', 'version': 'číslo_verzie', 'p': 'údaje_pozícia', 'selector': 'selektor', 'xvfb': 'virtuálny_displej', 'display': 'displej', 'n': 'položka_COUNT', 'key': '누름값', 'processes': '실행과정들', 'rootfs': '뿌리파일계층', 'xdo': 'virtuálny_vstup_nástroj', 'name': 'Názov', 'window': 'Okno', 'report': 'overenie_správa', 'work': '작업경로'}
    for 이전, v_termíne_splatnosti_položka in mapovanie_VALUE.items():
        if hasattr(구현, v_termíne_splatnosti_položka): globals()[이전] = getattr(구현, v_termíne_splatnosti_položka)
