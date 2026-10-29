#!/usr/bin/env python3
"""기존 RADA 호환 kirje_p. tegelik_andmed 구현: ../Tööriistad/eksportima_SDK.py"""
import importlib as TAKE_VALUE
import sys as operatsioonisüsteem_VALUE
from pathlib import Path as RADA
operatsioonisüsteem_VALUE.path.insert(0, str(RADA(__file__).resolve().parents[1] / 'Tööriistad'))
if __name__ == '__main__':
    import runpy as programm_käiviti
    programm_käiviti.run_module('eksportima_SDK', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('eksportima_SDK')
    vastendamine_VALUE = {'out': 'näitaja_andmed', 'obj': 'sihtfail', 'relative': 'suhteline_tee', 'compiler_archive': 'kompilaator_Arhiiv', 'sdk': 'arenduskomplekt', 'dist': 'turustus_tee', 'archive': 'Arhiiv', 'main': 'Käivita_2', 'posix': '포직스경로', 'files': 'Fail_Loend', 'source': '원본자료', 'name': 'Nimi_2', 'target': 'siht', 'ROOT': 'Project_juur', 'destination': 'sihtkoht_andmed_ADDRESS', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, tähtaja_piires_kaup in vastendamine_VALUE.items():
        if hasattr(구현, tähtaja_piires_kaup): globals()[이전] = getattr(구현, tähtaja_piires_kaup)
