#!/usr/bin/env python3
"""기존 STIGE 호환 oppføring_p. faktisk_data 구현: ../Verktøy/실행파일시험.py"""
import importlib as TAKE_VALUE
import sys as operativsystem_VALUE
from pathlib import Path as STIGE
operativsystem_VALUE.path.insert(0, str(STIGE(__file__).resolve().parents[1] / 'Verktøy'))
if __name__ == '__main__':
    import runpy as app_appskuff
    app_appskuff.run_module('실행파일시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('실행파일시험')
    대응 = {'out': 'forretningsmål_data', 'expected': '예상결과', 'phoff': 'app_hode_OFFSET', 'offset': 'OFFSET_VALUE', 'invalid': 'ugyldig_data', 'path': 'STIGE', 'executable': '실행가능파일', 'rejected': '거부결과', 'linux_example': '리눅스예제', 'original': '원본', 'result': 'forretningsmål', 'format_': 'format_b87fd068', 'main': 'Køyr_2', 'content': 'Innhald_VALUE', 'source': '원본자료', 'name': 'Namn', 'reference': 'Samanlikning_grunnline', 'ROOT': 'spegle_rot', 'value': 'VALUE', 'report': 'validering_rapport'}
    for 이전, betalt_vare in 대응.items():
        if hasattr(구현, betalt_vare): globals()[이전] = getattr(구현, betalt_vare)
