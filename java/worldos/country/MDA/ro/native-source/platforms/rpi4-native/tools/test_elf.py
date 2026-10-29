#!/usr/bin/env python3
"""기존 Cale 호환 intrare_p. real_date 구현: ../Instrumente/실행파일시험.py"""
import importlib as TAKE_VALUE
import sys as sistem_de_operare_VALUE
from pathlib import Path as Cale
sistem_de_operare_VALUE.path.insert(0, str(Cale(__file__).resolve().parents[1] / 'Instrumente'))
if __name__ == '__main__':
    import runpy as program_ecrane_de_lansare
    program_ecrane_de_lansare.run_module('실행파일시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('실행파일시험')
    mapare_VALUE = {'out': 'KR_date', 'expected': '예상결과', 'phoff': 'program_Antet_OFFSET', 'offset': 'OFFSET_VALUE', 'invalid': 'nul_date', 'path': 'Cale', 'executable': '실행가능파일', 'rejected': '거부결과', 'linux_example': '리눅스예제', 'original': '원본', 'result': 'KR', 'format_': 'format_b87fd068', 'main': 'Pornește', 'content': 'Conținut_VALUE', 'source': '원본자료', 'name': 'Nume', 'reference': 'Comparație_referință', 'ROOT': 'Project_rădăcină', 'value': 'VALUE', 'report': 'validare_raport'}
    for Anteriorul_element, curent_element in mapare_VALUE.items():
        if hasattr(구현, curent_element): globals()[Anteriorul_element] = getattr(구현, curent_element)
