#!/usr/bin/env python3
"""기존 Inzira 호환 icyinjizwa_inota. nyakuri_amakurushingiro 구현: ../Ibikoresho/터미널글꼴빌드.py"""
import importlib as 가져오기
import sys as sisitemu_ngengamikorere_agaciro
from pathlib import Path as Inzira
sisitemu_ngengamikorere_agaciro.path.insert(0, str(Inzira(__file__).resolve().parents[1] / 'Ibikoresho'))
if __name__ == '__main__':
    import runpy as porogaramu_umukozi
    porogaramu_umukozi.run_module('터미널글꼴빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('터미널글꼴빌드')
    대응 = {'data': 'amakurushingiro', 'img': 'igishushanyo_agaciro', 'bits': '비트들', 'x': 'Ihuza_rya_x', 'draw': '화면그리기', 'licences': '이용허락목록', 'paths': 'inzira_Urutonde', 'y': '세로좌표', 'main': 'ihuriro', 'src': '원본주소', 'fonts': 'imyandikire_Urutonde', 'ROOT': '기준', 'p': '자료위치', 'cp': 'inyuguti_gusobeka', 'target': 'gusimbuza_igishya'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
