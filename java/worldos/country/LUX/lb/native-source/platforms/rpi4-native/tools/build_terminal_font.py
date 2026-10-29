#!/usr/bin/env python3
"""기존 Wee 호환 Agab_Punkt. aktuell_Daten 구현: ../Tools/Build_Terminal_Schrëftaart.py"""
import importlib as TAKE_VALUE
import sys as Betribssystem_VALUE
from pathlib import Path as Wee
Betribssystem_VALUE.path.insert(0, str(Wee(__file__).resolve().parents[1] / 'Tools'))
if __name__ == '__main__':
    import runpy as App_App_Beräich
    App_App_Beräich.run_module('Build_Terminal_Schrëftaart', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('Build_Terminal_Schrëftaart')
    대응 = {'data': 'Daten', 'img': 'Zeechnung_VALUE', 'bits': '비트들', 'x': 'X_Koordinat', 'draw': '화면그리기', 'licences': '이용허락목록', 'paths': 'Wee_Lëscht', 'y': '세로좌표', 'main': 'Laf', 'src': '원본주소', 'fonts': 'Schrëftaart_Lëscht', 'ROOT': 'projezéieren_Racinn', 'p': 'Daten_positionéieren', 'cp': 'Zeechen_Codéierung', 'target': 'Zil'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
