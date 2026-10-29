#!/usr/bin/env python3
"""기존 ara 호환 tāurunga_ira. tūturu_raraunga 구현: ../Ngā_Utauta/hanga_Tauranga_momotuhi.py"""
import importlib as TAKE_uara
import sys as pūnaha_mahi_uara
from pathlib import Path as ara
pūnaha_mahi_uara.path.insert(0, str(ara(__file__).resolve().parents[1] / 'Ngā_Utauta'))
if __name__ == '__main__':
    import runpy as kaupapa_pūwhiri_taupānga
    kaupapa_pūwhiri_taupānga.run_module('hanga_Tauranga_momotuhi', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_uara.import_module('hanga_Tauranga_momotuhi')
    대응 = {'data': 'raraunga', 'img': 'tātuhi_uara', 'bits': '비트들', 'x': 'taunga_x', 'draw': '화면그리기', 'licences': '이용허락목록', 'paths': 'ara_Rārangi', 'y': '세로좌표', 'main': 'whakahaere', 'src': '원본주소', 'fonts': 'momotuhi_Rārangi', 'ROOT': 'whakaatu_pūtake', 'p': 'raraunga_tūranga', 'cp': 'pūāhua_whakawaehere', 'target': 'ūnga'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
