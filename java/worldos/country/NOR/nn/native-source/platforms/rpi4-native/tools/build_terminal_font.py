#!/usr/bin/env python3
"""기존 STIGE 호환 oppføring_p. faktisk_data 구현: ../Verktøy/bygg_Terminal_skrift.py"""
import importlib as TAKE_VALUE
import sys as operativsystem_VALUE
from pathlib import Path as STIGE
operativsystem_VALUE.path.insert(0, str(STIGE(__file__).resolve().parents[1] / 'Verktøy'))
if __name__ == '__main__':
    import runpy as app_appskuff
    app_appskuff.run_module('bygg_Terminal_skrift', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('bygg_Terminal_skrift')
    대응 = {'data': 'data', 'img': 'teikning_VALUE', 'bits': '비트들', 'x': 'x_koordinat', 'draw': '화면그리기', 'licences': '이용허락목록', 'paths': 'bane_Liste', 'y': 'Y_koordinat', 'main': 'Køyr_2', 'src': '원본주소', 'fonts': 'skrift_Liste', 'ROOT': 'spegle_rot', 'p': 'data_plassere', 'cp': 'teikn_koding', 'target': 'mål'}
    for 이전, betalt_vare in 대응.items():
        if hasattr(구현, betalt_vare): globals()[이전] = getattr(구현, betalt_vare)
