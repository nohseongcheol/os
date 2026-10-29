#!/usr/bin/env python3
"""기존 mogħdija 호환 entrata_punt. attwali_data 구현: ../Għodod/bena_Terminal_font.py"""
import importlib as TAKE_VALUE
import sys as sistema_operattiva_VALUE
from pathlib import Path as mogħdija
sistema_operattiva_VALUE.path.insert(0, str(mogħdija(__file__).resolve().parents[1] / 'Għodod'))
if __name__ == '__main__':
    import runpy as programm_ġabra_ta_apps
    programm_ġabra_ta_apps.run_module('bena_Terminal_font', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('bena_Terminal_font')
    대응 = {'data': 'data', 'img': 'tpinġija_VALUE', 'bits': '비트들', 'x': 'koordinat_x', 'draw': '화면그리기', 'licences': '이용허락목록', 'paths': 'mogħdija_Lista', 'y': '세로좌표', 'main': 'serje', 'src': '원본주소', 'fonts': 'font_Lista', 'ROOT': 'pprojetta_għerq', 'p': 'data_pożizzjoni', 'cp': 'karattru_kodifikar', 'target': 'mira'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
