#!/usr/bin/env python3
"""기존 Slighe 호환 cur_a_steach_puing. dearbh_dàta 구현: ../innealan/tog_tèirmineal_cruth_clò.py"""
import importlib as TAKE_VALUE
import sys as siostam_obrachaidh_VALUE
from pathlib import Path as Slighe
siostam_obrachaidh_VALUE.path.insert(0, str(Slighe(__file__).resolve().parents[1] / 'innealan'))
if __name__ == '__main__':
    import runpy as ap_drathair_nan_aplacaid
    ap_drathair_nan_aplacaid.run_module('tog_tèirmineal_cruth_clò', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('tog_tèirmineal_cruth_clò')
    대응 = {'data': 'dàta', 'img': 'tarraing_VALUE', 'bits': '비트들', 'x': 'co_chomharra_x', 'draw': '화면그리기', 'licences': '이용허락목록', 'paths': 'slighe_Liosta', 'y': '세로좌표', 'main': 'ruith', 'src': '원본주소', 'fonts': 'cruth_clò_Liosta', 'ROOT': 'tilg_freumh', 'p': 'dàta_suidhich', 'cp': 'caractar_còdachadh', 'target': 'targaid'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
