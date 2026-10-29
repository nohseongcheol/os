#!/usr/bin/env python3
"""기존 Tsejana 호환 go_tsenya_tshedimošo_ntlha. kgonthe_data 구현: ../Ditholosi/터미널글꼴빌드.py"""
import importlib as 가져오기
import sys as tshepedišotirišo_boleng
from pathlib import Path as Tsejana
tshepedišotirišo_boleng.path.insert(0, str(Tsejana(__file__).resolve().parents[1] / 'Ditholosi'))
if __name__ == '__main__':
    import runpy as tirišo_sethala_tirišo
    tirišo_sethala_tirišo.run_module('터미널글꼴빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('터미널글꼴빌드')
    대응 = {'data': 'data', 'img': 'sethalwa_boleng', 'bits': '비트들', 'x': 'kamano_ya_x', 'draw': '화면그리기', 'licences': '이용허락목록', 'paths': 'tsela_Lenaneo', 'y': '세로좌표', 'main': 'Diriša', 'src': '원본주소', 'fonts': 'fonte_Lenaneo', 'ROOT': '기준', 'p': '자료위치', 'cp': 'tlhaka_go_enkhouta', 'target': 'nepo'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
