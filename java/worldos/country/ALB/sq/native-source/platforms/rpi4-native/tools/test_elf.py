#!/usr/bin/env python3
"""기존 POZICIONI 호환 futje_p. aktual_të_dhëna 구현: ../Mjete/실행파일시험.py"""
import importlib as TAKE_VALUE
import sys as sistem_operativ_VALUE
from pathlib import Path as POZICIONI
sistem_operativ_VALUE.path.insert(0, str(POZICIONI(__file__).resolve().parents[1] / 'Mjete'))
if __name__ == '__main__':
    import runpy as program_hapës
    program_hapës.run_module('실행파일시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('실행파일시험')
    대응 = {'out': 'llogaritje_të_dhëna', 'expected': '예상결과', 'phoff': 'program_Kreu_OFFSET', 'offset': 'OFFSET_VALUE', 'invalid': 'i_pavlefshëm_të_dhëna', 'path': 'POZICIONI', 'executable': '실행가능파일', 'rejected': '거부결과', 'linux_example': '리눅스예제', 'original': '원본', 'result': 'llogaritje', 'format_': 'format_b87fd068', 'main': 'Ekzekuto', 'content': 'Përmbajtje_VALUE', 'source': '원본자료', 'name': 'Emër', 'reference': 'Krahasim_vijëbazë', 'ROOT': 'Project_rrënjë', 'value': 'VALUE', 'report': 'miratim_raport'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
