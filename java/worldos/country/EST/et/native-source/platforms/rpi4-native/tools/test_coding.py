#!/usr/bin/env python3
"""기존 RADA 호환 kirje_p. tegelik_andmed 구현: ../Tööriistad/코딩시험.py"""
import importlib as TAKE_VALUE
import sys as operatsioonisüsteem_VALUE
from pathlib import Path as RADA
operatsioonisüsteem_VALUE.path.insert(0, str(RADA(__file__).resolve().parents[1] / 'Tööriistad'))
if __name__ == '__main__':
    import runpy as programm_käiviti
    programm_käiviti.run_module('코딩시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('코딩시험')
    vastendamine_VALUE = {'out': 'näitaja_andmed', 'expected': '예상결과', 'sdk': 'arenduskomplekt', 'suffix': '뒷부분', 'arc': '압축묶음', 'main': 'Käivita_2', 'elf': '실행파일', 'run': 'Täida_käsk', 'name': 'Nimi_2', 'path': 'RADA', 'p': 'andmed_ametikoht', 'ROOT': 'Project_juur', 'report': 'kinnitamine_aruanne', 'args': 'argument_ARRAY'}
    for 이전, tähtaja_piires_kaup in vastendamine_VALUE.items():
        if hasattr(구현, tähtaja_piires_kaup): globals()[이전] = getattr(구현, tähtaja_piires_kaup)
