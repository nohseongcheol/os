#!/usr/bin/env python3
"""기존 RADA 호환 kirje_p. tegelik_andmed 구현: ../Tööriistad/järk_15_kompilaator.py"""
import importlib as TAKE_VALUE
import sys as operatsioonisüsteem_VALUE
from pathlib import Path as RADA
operatsioonisüsteem_VALUE.path.insert(0, str(RADA(__file__).resolve().parents[1] / 'Tööriistad'))
if __name__ == '__main__':
    import runpy as programm_käiviti
    programm_käiviti.run_module('järk_15_kompilaator', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('järk_15_kompilaator')
    vastendamine_VALUE = {'out': 'näitaja_andmed', 'builtins': '내장연산', 'header': 'Päis_VALUE', 'sdk': 'arenduskomplekt', 'build_ccompiler': 'avama_15_kompilaator', 'i': '순번', 'elf': '실행파일', 'run': 'Täida_käsk', 'flags': 'konfiguratsioon_Taustal_töötav_intelligentne_edastusteenus', 'path': 'RADA', 'p': 'andmed_ametikoht', 'cc': '_15_kompilaator', 'obj': 'sihtfail', 'flag': 'Sätted_VALUE', 'ld': '연결편집기', 'objects': 'sihtkoht_Failid', 'repo': 'hoidla_tee', 'v': '임시값', 'upstream': 'ülesvoolu', 'root': 'juur_ADDRESS', 'assets': '탑재자료', 'source': '원본자료', 'name': 'Nimi_2', 'includes': '포함인수'}
    for 이전, tähtaja_piires_kaup in vastendamine_VALUE.items():
        if hasattr(구현, tähtaja_piires_kaup): globals()[이전] = getattr(구현, tähtaja_piires_kaup)
