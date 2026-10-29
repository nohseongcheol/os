#!/usr/bin/env python3
"""기존 RADA 호환 kirje_p. tegelik_andmed 구현: ../Tööriistad/셸시험.py"""
import importlib as TAKE_VALUE
import sys as operatsioonisüsteem_VALUE
from pathlib import Path as RADA
operatsioonisüsteem_VALUE.path.insert(0, str(RADA(__file__).resolve().parents[1] / 'Tööriistad'))
if __name__ == '__main__':
    import runpy as programm_käiviti
    programm_käiviti.run_module('셸시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('셸시험')
    vastendamine_VALUE = {'timeout': '시간제한', 'x': '가로좌표', 'msg': 'võrk_meil', 'i': '순번', 'reply': 'vastus', 'call': '호출', 'args': 'argument_ARRAY', 'chunk': '조각', 'data': 'andmed', 'proc': 'Protsess', 'long_text': '긴글', 'restored': '복원자료', 'send': 'saatma', 'file': 'Fail', 'main': 'Käivita_2', 'found': 'Otsi_näitaja', 'ROOT': 'Project_juur', 'text': 'Tekst', 'marker': 'marker', 'command': 'Käsk', 'expected': '예상결과', 'pixel': 'piksel', 'shell': 'kest', 'poll': '준비살피미', 'transcript': 'transkriptsioon', 'end': 'lõpeta_kõne_nihe', 'image': 'pilt', 'key': '누름값', 'y': '세로좌표', 'output': 'toodang', 'result': 'TULEMUS', 'client': 'klient', 'line': 'Joon', 'stream': 'voog_VALUE', 'name': 'Nimi_2', 'value': 'VALUE', 'receive': 'saama_meil', 'report': 'kinnitamine_aruanne', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, tähtaja_piires_kaup in vastendamine_VALUE.items():
        if hasattr(구현, tähtaja_piires_kaup): globals()[이전] = getattr(구현, tähtaja_piires_kaup)
