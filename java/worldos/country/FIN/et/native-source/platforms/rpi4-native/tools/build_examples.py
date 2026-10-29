#!/usr/bin/env python3
"""기존 RADA 호환 kirje_p. tegelik_andmed 구현: ../Tööriistad/예제빌드.py"""
import importlib as TAKE_VALUE
import sys as operatsioonisüsteem_VALUE
from pathlib import Path as RADA
operatsioonisüsteem_VALUE.path.insert(0, str(RADA(__file__).resolve().parents[1] / 'Tööriistad'))
if __name__ == '__main__':
    import runpy as programm_käiviti
    programm_käiviti.run_module('예제빌드', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('예제빌드')
    vastendamine_VALUE = {'out': 'näitaja_andmed', 'build_examples': '예제만들기', 'files': 'Fail_Loend', 'java': '자바실행', 'run': 'Täida_käsk', 'path': 'RADA', 'p': 'andmed_ametikoht', 'readme': '안내자료', 'build_java_library': '자바라이브러리만들기', 'code': '명령열', 'index': 'LOOKUP_INDEX', 'classes': 'tund_tee', 'repo': 'hoidla_tee', 'root': 'juur_ADDRESS', 'content': 'Sisu_VALUE', 'source': '원본자료', 'name': 'Nimi_2', 'target': 'siht', 'manifest': '꾸러미명세', 'language': 'Keeled'}
    for 이전, tähtaja_piires_kaup in vastendamine_VALUE.items():
        if hasattr(구현, tähtaja_piires_kaup): globals()[이전] = getattr(구현, tähtaja_piires_kaup)
