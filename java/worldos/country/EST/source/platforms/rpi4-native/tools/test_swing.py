#!/usr/bin/env python3
"""기존 RADA 호환 kirje_p. tegelik_andmed 구현: ../Tööriistad/화면요소시험.py"""
import importlib as TAKE_VALUE
import sys as operatsioonisüsteem_VALUE
from pathlib import Path as RADA
operatsioonisüsteem_VALUE.path.insert(0, str(RADA(__file__).resolve().parents[1] / 'Tööriistad'))
if __name__ == '__main__':
    import runpy as programm_käiviti
    programm_käiviti.run_module('화면요소시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('화면요소시험')
    vastendamine_VALUE = {'wait': '기다리기', 'x': '가로좌표', 's': 'string_andmed', 'i': '순번', 'sel': 'valija_a916db4e', 'seconds': '초단위', 'log': 'LOG_kirje', 'data': 'andmed', 'at': 'tähtaja_piires_ametikoht', 'send': 'saatma', 'main': 'Käivita_2', 'req': 'päring_VALUE_625fa62c', 'hot': 'otsetee_VALUE', 'pump': 'pide_sündmus', 'ROOT': 'Project_juur', 'marker': 'marker', 'b': 'SECOND_VALUE', 'command': 'Käsk', 'shell': 'kest', 'f': 'Fail_kirje', 'click': 'klõps_nupp', 'k': '셋째순번', 'c': 'koodipunkt', 'r': '반환값', 'p': 'andmed_ametikoht', 'command_mode': 'käsk_MODE', 'end': 'lõpeta_kõne_nihe', 'classes': 'tund_tee', 'key': '누름값', 'y': '세로좌표', 'result': 'TULEMUS', 'report': 'kinnitamine_aruanne', 'dest': 'sihtkoht_VALUE_ametikoht', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, tähtaja_piires_kaup in vastendamine_VALUE.items():
        if hasattr(구현, tähtaja_piires_kaup): globals()[이전] = getattr(구현, tähtaja_piires_kaup)
