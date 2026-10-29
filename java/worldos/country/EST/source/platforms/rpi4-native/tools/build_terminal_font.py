#!/usr/bin/env python3
"""기존 RADA 호환 kirje_p. tegelik_andmed 구현: ../Tööriistad/järk_terminal_font.py"""
import importlib as TAKE_VALUE
import sys as operatsioonisüsteem_VALUE
from pathlib import Path as RADA
operatsioonisüsteem_VALUE.path.insert(0, str(RADA(__file__).resolve().parents[1] / 'Tööriistad'))
if __name__ == '__main__':
    import runpy as programm_käiviti
    programm_käiviti.run_module('järk_terminal_font', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('järk_terminal_font')
    vastendamine_VALUE = {'data': 'andmed', 'img': 'joonis_VALUE', 'bits': 'Taustal_töötav_intelligentne_edastusteenus_Loend', 'x': '가로좌표', 'draw': '화면그리기', 'licences': '이용허락목록', 'paths': 'tee_Loend', 'y': '세로좌표', 'main': 'Käivita_2', 'src': '원본주소', 'fonts': 'font_Loend', 'ROOT': 'Project_juur', 'p': 'andmed_ametikoht', 'cp': 'märk_kodeerimine', 'target': 'siht'}
    for 이전, tähtaja_piires_kaup in vastendamine_VALUE.items():
        if hasattr(구현, tähtaja_piires_kaup): globals()[이전] = getattr(구현, tähtaja_piires_kaup)
