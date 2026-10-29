#!/usr/bin/env python3
"""기존 STIGE 호환 oppføring_p. faktisk_data 구현: ../Verktøy/개발꾸러미내보내기.py"""
import importlib as TAKE_VALUE
import sys as operativsystem_VALUE
from pathlib import Path as STIGE
operativsystem_VALUE.path.insert(0, str(STIGE(__file__).resolve().parents[1] / 'Verktøy'))
if __name__ == '__main__':
    import runpy as app_appskuff
    app_appskuff.run_module('개발꾸러미내보내기', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('개발꾸러미내보내기')
    대응 = {'out': 'forretningsmål_data', 'obj': 'målfil', 'relative': '상대경로', 'compiler_archive': '번역기꾸러미', 'sdk': '개발꾸러미', 'dist': '배포경로', 'archive': 'Arkiv', 'main': 'Køyr_2', 'posix': '포직스경로', 'files': 'fil_Liste', 'source': '원본자료', 'name': 'Namn', 'target': 'mål', 'ROOT': 'spegle_rot', 'destination': 'mål_data_ADDRESS', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, betalt_vare in 대응.items():
        if hasattr(구현, betalt_vare): globals()[이전] = getattr(구현, betalt_vare)
