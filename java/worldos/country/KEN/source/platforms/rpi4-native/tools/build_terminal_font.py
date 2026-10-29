#!/usr/bin/env python3
"""기존 njia 호환 ingizo_pointi. halisi_data 구현: ../Zana/터미널글꼴빌드.py"""
import importlib as 가져오기
import sys as mfumo_endeshi_thamani
from pathlib import Path as njia
mfumo_endeshi_thamani.path.insert(0, str(njia(__file__).resolve().parents[1] / 'Zana'))
if __name__ == '__main__':
    import runpy as programu_droo_ya_programu
    programu_droo_ya_programu.run_module('터미널글꼴빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('터미널글꼴빌드')
    대응 = {'data': 'data', 'img': 'mchoro_thamani', 'bits': 'Huduma_ya_Uhamisho_wa_Ujasusi_wa_Mandharinyuma_Orodha', 'x': 'jira_x', 'draw': '화면그리기', 'licences': '이용허락목록', 'paths': 'njia_Orodha', 'y': 'Kitufe_cha_Y_kiratibu', 'main': 'endesha', 'src': '원본주소', 'fonts': 'fonti_Orodha', 'ROOT': '기준', 'p': '자료위치', 'cp': 'kibambo_usimbaji', 'target': 'lengo'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
