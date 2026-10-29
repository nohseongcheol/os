#!/usr/bin/env python3
"""기존 RADA 호환 kirje_p. tegelik_andmed 구현: ../Tööriistad/Upload_Failid.py"""
import importlib as TAKE_VALUE
import sys as operatsioonisüsteem_VALUE
from pathlib import Path as RADA
operatsioonisüsteem_VALUE.path.insert(0, str(RADA(__file__).resolve().parents[1] / 'Tööriistad'))
if __name__ == '__main__':
    import runpy as programm_käiviti
    programm_käiviti.run_module('Upload_Failid', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('Upload_Failid')
    vastendamine_VALUE = {'data': 'andmed', 'i': '순번', 'name': 'Nimi_2', 'c': 'koodipunkt', 'p': 'andmed_ametikoht', 'args': 'argument_ARRAY'}
    for 이전, tähtaja_piires_kaup in vastendamine_VALUE.items():
        if hasattr(구현, tähtaja_piires_kaup): globals()[이전] = getattr(구현, tähtaja_piires_kaup)
