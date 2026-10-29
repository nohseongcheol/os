#!/usr/bin/env python3
"""기존 Pad 호환 inskrywing_p. werklik_data 구현: ../Nutsmiddels/bou_Terminaal_font.py"""
import importlib as TAKE_VALUE
import sys as bedryfstelsel_VALUE
from pathlib import Path as Pad
bedryfstelsel_VALUE.path.insert(0, str(Pad(__file__).resolve().parents[1] / 'Nutsmiddels'))
if __name__ == '__main__':
    import runpy as program_oopmaker
    program_oopmaker.run_module('bou_Terminaal_font', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('bou_Terminaal_font')
    대응 = {'data': 'data', 'img': 'tekening_VALUE', 'bits': 'Agtergrond_intelligente_oordragdiens_Lys', 'x': 'x_koördinaat', 'draw': '화면그리기', 'licences': '이용허락목록', 'paths': 'pad_Lys', 'y': 'Y_koördinaat', 'main': 'Loop', 'src': '원본주소', 'fonts': 'font_Lys', 'ROOT': 'Project_wortel', 'p': 'data_plaas', 'cp': 'karakter_enkodering', 'target': 'teiken'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
