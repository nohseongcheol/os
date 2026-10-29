#!/usr/bin/env python3
"""기존 Pad 호환 inskrywing_p. werklik_data 구현: ../Nutsmiddels/자바라이브러리빌드.py"""
import importlib as TAKE_VALUE
import sys as bedryfstelsel_VALUE
from pathlib import Path as Pad
bedryfstelsel_VALUE.path.insert(0, str(Pad(__file__).resolve().parents[1] / 'Nutsmiddels'))
if __name__ == '__main__':
    import runpy as program_oopmaker
    program_oopmaker.run_module('자바라이브러리빌드', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('자바라이브러리빌드')
    대응 = {'header': 'Loopkop_VALUE', 'sources': '원문목록', 'i': '순번', 'info': 'Stelselinfo', 'payload': 'lading_data', 'src': '원본주소', 'run': 'uitvoer_bevel', 'build_java_library': '자바라이브러리만들기', 'relative': '상대경로', 'classes': 'Klas_pad', 'dist': '배포경로', 'archive': 'Argief', 'output': '출력결과', 'root': 'wortel_adres', 'name': 'Naam', 'jar': '자바꾸러미', 'b': 'SECOND_VALUE', 'entries': '항목들'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
