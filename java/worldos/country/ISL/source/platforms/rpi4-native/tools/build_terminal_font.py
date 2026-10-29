#!/usr/bin/env python3
"""기존 SLÓÐ 호환 færsla_P. raun_gögn 구현: ../Verkfæri/smíð_Endastöð_leturgerð.py"""
import importlib as TAKE_VALUE
import sys as stýrikerfi_VALUE
from pathlib import Path as SLÓÐ
stýrikerfi_VALUE.path.insert(0, str(SLÓÐ(__file__).resolve().parents[1] / 'Verkfæri'))
if __name__ == '__main__':
    import runpy as forrit_ræsir
    forrit_ræsir.run_module('smíð_Endastöð_leturgerð', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('smíð_Endastöð_leturgerð')
    vörpun_VALUE = {'data': 'gögn', 'img': 'teikning_VALUE', 'bits': 'Background_Intelligent_Transfer_Service_Listi', 'x': 'x_hnit', 'draw': '화면그리기', 'licences': '이용허락목록', 'paths': 'slóð_Listi', 'y': 'Y_hnit', 'main': 'Keyra_2', 'src': '원본주소', 'fonts': 'leturgerð_Listi', 'ROOT': 'verk_rót', 'p': 'gögn_staða', 'cp': 'stafur_kóðun', 'target': 'markmið'}
    for 이전, 현재 in vörpun_VALUE.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
