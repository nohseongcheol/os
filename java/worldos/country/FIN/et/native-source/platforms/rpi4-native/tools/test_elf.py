#!/usr/bin/env python3
"""기존 RADA 호환 kirje_p. tegelik_andmed 구현: ../Tööriistad/실행파일시험.py"""
import importlib as TAKE_VALUE
import sys as operatsioonisüsteem_VALUE
from pathlib import Path as RADA
operatsioonisüsteem_VALUE.path.insert(0, str(RADA(__file__).resolve().parents[1] / 'Tööriistad'))
if __name__ == '__main__':
    import runpy as programm_käiviti
    programm_käiviti.run_module('실행파일시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('실행파일시험')
    vastendamine_VALUE = {'out': 'näitaja_andmed', 'expected': '예상결과', 'phoff': 'programm_Päis_nihe', 'offset': 'nihe_VALUE', 'invalid': 'kehtetu_andmed', 'path': 'RADA', 'executable': '실행가능파일', 'rejected': '거부결과', 'linux_example': '리눅스예제', 'original': '원본', 'result': 'TULEMUS', 'format_': 'vorming_b87fd068', 'main': 'Käivita_2', 'content': 'Sisu_VALUE', 'source': '원본자료', 'name': 'Nimi_2', 'reference': 'Võrdlus_alusjoon', 'ROOT': 'Project_juur', 'value': 'VALUE', 'report': 'kinnitamine_aruanne'}
    for 이전, tähtaja_piires_kaup in vastendamine_VALUE.items():
        if hasattr(구현, tähtaja_piires_kaup): globals()[이전] = getattr(구현, tähtaja_piires_kaup)
