#!/usr/bin/env python3
"""기존 Ýol 호환 girizmeklik_utuk. hakyky_maglumat 구현: ../Gurallar/창시험.py"""
import importlib as 가져오기
import sys as operasiýa_ulgamy_baha
from pathlib import Path as Ýol
operasiýa_ulgamy_baha.path.insert(0, str(Ýol(__file__).resolve().parents[1] / 'Gurallar'))
if __name__ == '__main__':
    import runpy as programma_programma_paneli
    programma_programma_paneli.run_module('창시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('창시험')
    대응 = {'wait': '기다리기', 'x': 'x_koordinatasy', 's': 'setir_maglumat', 'xy': 'koordinata_jübüti', 'sel': 'saýlaýjy_a916db4e', 'seconds': '초단위', 'log': 'hasaba_alyş_setir', 'at': '현재위치', 'send': 'iber', 'main': 'Bitir', 'req': '요청값', 'hot': 'ýarlyk_baha', 'pump': 'ryçag_waka', 'ROOT': '기준', 'marker': '확인표시', 'b': '둘째값', 'command': 'buýruk', 'shell': 'gabyjak', 'f': 'faýl_girizmeklik', 'color': '색상', 'click': 'bas_düwme', 'k': '셋째순번', 'c': 'nyşanyň_kody', 'r': '반환값', 'p': '자료위치', 'done': '완료량', 'end': 'tamamla_Süýşüriş', 'command_mode': 'buýruk_reje', 'key': '누름값', 'y': '세로좌표', 'pixels': '화소들', 'result': '결과', 'report': 'barlag_hasabat', 'dest': '목적위치', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
