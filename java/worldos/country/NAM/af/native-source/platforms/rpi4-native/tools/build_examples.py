#!/usr/bin/env python3
"""기존 Pad 호환 inskrywing_p. werklik_data 구현: ../Nutsmiddels/예제빌드.py"""
import importlib as TAKE_VALUE
import sys as bedryfstelsel_VALUE
from pathlib import Path as Pad
bedryfstelsel_VALUE.path.insert(0, str(Pad(__file__).resolve().parents[1] / 'Nutsmiddels'))
if __name__ == '__main__':
    import runpy as program_oopmaker
    program_oopmaker.run_module('예제빌드', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('예제빌드')
    대응 = {'out': 'maatreël_data', 'build_examples': '예제만들기', 'files': 'lêer_Lys', 'java': '자바실행', 'run': 'uitvoer_bevel', 'path': 'Pad', 'p': 'data_plaas', 'readme': 'README', 'build_java_library': '자바라이브러리만들기', 'code': 'instruksie_SEQUENCE', 'index': 'LOOKUP_INDEX', 'classes': 'Klas_pad', 'repo': 'bewaarplek_pad', 'root': 'wortel_adres', 'content': 'Inhoud_VALUE', 'source': '원본자료', 'name': 'Naam', 'target': 'teiken', 'manifest': '꾸러미명세', 'language': 'Taal'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
