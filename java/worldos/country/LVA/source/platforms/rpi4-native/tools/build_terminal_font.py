#!/usr/bin/env python3
"""기존 CEĻŠ 호환 ieejas_punkts. faktisks_dati 구현: ../Rīki/būvējums_Terminālis_fonts.py"""
import importlib as TAKE_VALUE
import sys as operētājsistēma_VALUE
from pathlib import Path as CEĻŠ
operētājsistēma_VALUE.path.insert(0, str(CEĻŠ(__file__).resolve().parents[1] / 'Rīki'))
if __name__ == '__main__':
    import runpy as programma_palaidējs
    programma_palaidējs.run_module('būvējums_Terminālis_fonts', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('būvējums_Terminālis_fonts')
    kartēšana_VALUE = {'data': 'dati', 'img': 'zīmējums_VALUE', 'bits': 'Background_Intelligent_Transfer_Service_Saraksts', 'x': 'x_koordināta', 'draw': '화면그리기', 'licences': '이용허락목록', 'paths': 'ceļš_Saraksts', 'y': '세로좌표', 'main': 'Palaist', 'src': '원본주소', 'fonts': 'fonts_Saraksts', 'ROOT': 'Project_sakne', 'p': 'dati_amats', 'cp': 'rakstzīmju_kodēšana', 'target': 'mērķis'}
    for 이전, pašreizējais_krājums in kartēšana_VALUE.items():
        if hasattr(구현, pašreizējais_krājums): globals()[이전] = getattr(구현, pašreizējais_krājums)
