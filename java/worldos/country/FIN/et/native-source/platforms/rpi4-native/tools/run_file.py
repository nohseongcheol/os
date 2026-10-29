#!/usr/bin/env python3
"""기존 RADA 호환 kirje_p. tegelik_andmed 구현: ../Tööriistad/Täida_Fail.py"""
import importlib as TAKE_VALUE
import sys as operatsioonisüsteem_VALUE
from pathlib import Path as RADA
operatsioonisüsteem_VALUE.path.insert(0, str(RADA(__file__).resolve().parents[1] / 'Tööriistad'))
if __name__ == '__main__':
    import runpy as programm_käiviti
    programm_käiviti.run_module('Täida_Fail', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('Täida_Fail')
    vastendamine_VALUE = {'timeout': '시간제한', 's': 'string_andmed', 'i': '순번', 'match': '일치', 'files': 'Fail_Loend', 'program': 'programm', 'executable': '실행가능파일', 'args': 'argument_ARRAY', 'chunk': '조각', 'data': 'andmed', 'proc': 'Protsess', 'send': 'saatma', 'main': 'Käivita_2', 'marker': 'marker', 'command': 'Käsk', 'include': 'hõlmama', 'dumped': '갈무리자료', 'run': 'Täida_käsk', 'p': 'andmed_ametikoht', 'parser': 'parser', 'options': 'Suvandid', 'kind': 'ala_VALUE', 'selector': 'valija', 'upload_data': 'Upload_andmed', 'end': 'lõpeta_kõne_nihe', 'n': 'kaup_COUNT', 'd': 'sihtkoht_andmed', 'key': '누름값', 'output': 'toodang', 'line': 'Joon', 'name': 'Nimi_2', 'upload_name': 'Upload_nimetus', 'receive': 'saama_meil'}
    for 이전, tähtaja_piires_kaup in vastendamine_VALUE.items():
        if hasattr(구현, tähtaja_piires_kaup): globals()[이전] = getattr(구현, tähtaja_piires_kaup)
