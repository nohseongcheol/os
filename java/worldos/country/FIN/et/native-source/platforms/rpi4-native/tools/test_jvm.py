#!/usr/bin/env python3
"""기존 RADA 호환 kirje_p. tegelik_andmed 구현: ../Tööriistad/자바가상기계시험.py"""
import importlib as TAKE_VALUE
import sys as operatsioonisüsteem_VALUE
from pathlib import Path as RADA
operatsioonisüsteem_VALUE.path.insert(0, str(RADA(__file__).resolve().parents[1] / 'Tööriistad'))
if __name__ == '__main__':
    import runpy as programm_käiviti
    programm_käiviti.run_module('자바가상기계시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('자바가상기계시험')
    vastendamine_VALUE = {'message': 'teatamine_SMS', 's': 'string_andmed', 'actual': 'tegelik_näitaja', 'match': '일치', 'payload': 'last_andmed', 'cases': '시험사례', 'fixture': '시험자료', 'main': 'Käivita_2', 'ROOT': 'Project_juur', 'text': 'Tekst', 'valid': '유효함', 'includes': '포함인수', 'include': 'hõlmama', 'expected': '예상결과', 'sources': '원문목록', 'tmp': '임시경로', 'done': 'Lõpetatud_kogus', 'classes': 'tund_tee', 'output': 'toodang', 'result': 'TULEMUS', 'cmd': '명령인수', 'name': 'Nimi_2', 'jar': '자바꾸러미', 'report': 'kinnitamine_aruanne', 'tests': '시험목록'}
    for 이전, tähtaja_piires_kaup in vastendamine_VALUE.items():
        if hasattr(구현, tähtaja_piires_kaup): globals()[이전] = getattr(구현, tähtaja_piires_kaup)
