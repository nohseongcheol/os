#!/usr/bin/env python3
"""기존 Pad 호환 inskrywing_p. werklik_data 구현: ../Nutsmiddels/실행파일시험.py"""
import importlib as TAKE_VALUE
import sys as bedryfstelsel_VALUE
from pathlib import Path as Pad
bedryfstelsel_VALUE.path.insert(0, str(Pad(__file__).resolve().parents[1] / 'Nutsmiddels'))
if __name__ == '__main__':
    import runpy as program_oopmaker
    program_oopmaker.run_module('실행파일시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('실행파일시험')
    대응 = {'out': 'maatreël_data', 'expected': '예상결과', 'phoff': 'program_Loopkop_OFFSET', 'offset': 'OFFSET_VALUE', 'invalid': 'ongeldig_data', 'path': 'Pad', 'executable': '실행가능파일', 'rejected': '거부결과', 'linux_example': '리눅스예제', 'original': '원본', 'result': 'maatreël', 'format_': 'formaat_b87fd068', 'main': 'Loop', 'content': 'Inhoud_VALUE', 'source': '원본자료', 'name': 'Naam', 'reference': 'Vergelyking_basislyn', 'ROOT': 'Project_wortel', 'value': 'VALUE', 'report': 'validering_verslag'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
