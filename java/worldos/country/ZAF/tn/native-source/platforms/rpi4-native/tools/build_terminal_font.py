#!/usr/bin/env python3
"""기존 tsela 호환 tsenyo_ntlha. tota_tshedimosetso 구현: ../Thuluse/터미널글꼴빌드.py"""
import importlib as 가져오기
import sys as Tsamaisotiriso_Boleng
from pathlib import Path as tsela
Tsamaisotiriso_Boleng.path.insert(0, str(tsela(__file__).resolve().parents[1] / 'Thuluse'))
if __name__ == '__main__':
    import runpy as Tiriso_llae_ya_sediriso
    Tiriso_llae_ya_sediriso.run_module('터미널글꼴빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('터미널글꼴빌드')
    대응 = {'data': 'tshedimosetso', 'img': 'sethalo_Boleng', 'bits': '비트들', 'x': 'kgokagano_ya_x', 'draw': '화면그리기', 'licences': '이용허락목록', 'paths': 'tsela_lenaane', 'y': '세로좌표', 'main': 'dirisa', 'src': '원본주소', 'fonts': 'mofutatlhaka_lenaane', 'ROOT': '기준', 'p': '자료위치', 'cp': 'Letshwao_khoutufatso', 'target': 'setotwa'}
    for 이전, ga_jaana_selwana in 대응.items():
        if hasattr(구현, ga_jaana_selwana): globals()[이전] = getattr(구현, ga_jaana_selwana)
