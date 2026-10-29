#!/usr/bin/env python3
"""기존 Pad 호환 inskrywing_p. werklik_data 구현: ../Nutsmiddels/시언어번역기빌드.py"""
import importlib as TAKE_VALUE
import sys as bedryfstelsel_VALUE
from pathlib import Path as Pad
bedryfstelsel_VALUE.path.insert(0, str(Pad(__file__).resolve().parents[1] / 'Nutsmiddels'))
if __name__ == '__main__':
    import runpy as program_oopmaker
    program_oopmaker.run_module('시언어번역기빌드', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('시언어번역기빌드')
    대응 = {'out': 'maatreël_data', 'builtins': '내장연산', 'header': 'Loopkop_VALUE', 'sdk': '개발꾸러미', 'build_ccompiler': '시언어번역기만들기', 'i': '순번', 'elf': '실행파일', 'run': 'uitvoer_bevel', 'flags': 'konfigurasie_Agtergrond_intelligente_oordragdiens', 'path': 'Pad', 'p': 'data_plaas', 'cc': '시언어번역기', 'obj': 'bestemmingslêer', 'flag': 'Instellings_VALUE', 'ld': '연결편집기', 'objects': 'bestemming_Lêers', 'repo': 'bewaarplek_pad', 'v': '임시값', 'upstream': 'stroomop', 'root': 'wortel_adres', 'assets': '탑재자료', 'source': '원본자료', 'name': 'Naam', 'includes': '포함인수'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
