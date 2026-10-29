#!/usr/bin/env python3
"""기존 POZICIONI 호환 futje_p. aktual_të_dhëna 구현: ../Mjete/화면요소시험.py"""
import importlib as TAKE_VALUE
import sys as sistem_operativ_VALUE
from pathlib import Path as POZICIONI
sistem_operativ_VALUE.path.insert(0, str(POZICIONI(__file__).resolve().parents[1] / 'Mjete'))
if __name__ == '__main__':
    import runpy as program_hapës
    program_hapës.run_module('화면요소시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('화면요소시험')
    대응 = {'wait': '기다리기', 'x': 'koordinata_x', 's': 'varg_të_dhëna', 'i': '순번', 'sel': 'përzgjedhësi_a916db4e', 'seconds': '초단위', 'log': 'LOG_RECORD', 'data': 'të_dhëna', 'at': '현재위치', 'send': 'dërgoj', 'main': 'Ekzekuto', 'req': '요청값', 'hot': 'shkurtore_VALUE', 'pump': 'dorezë_ngjarje', 'ROOT': 'Project_rrënjë', 'marker': '확인표시', 'b': 'SECOND_VALUE', 'command': 'Komanda', 'shell': 'pasues', 'f': 'skedar_futje', 'click': 'klik_buton', 'k': '셋째순번', 'c': 'kodi_i_karakterit', 'r': '반환값', 'p': 'të_dhëna_pozicioni', 'command_mode': 'komandë_MODE', 'end': 'mbaroj_OFFSET', 'classes': 'klasë_shteg', 'key': '누름값', 'y': 'Y_koordinatë', 'result': 'llogaritje', 'report': 'miratim_raport', 'dest': 'vendmbërritje_VALUE_pozicioni', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
