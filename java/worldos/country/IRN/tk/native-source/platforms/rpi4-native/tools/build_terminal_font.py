#!/usr/bin/env python3
"""기존 Ýol 호환 girizmeklik_utuk. hakyky_maglumat 구현: ../Gurallar/터미널글꼴빌드.py"""
import importlib as 가져오기
import sys as operasiýa_ulgamy_baha
from pathlib import Path as Ýol
operasiýa_ulgamy_baha.path.insert(0, str(Ýol(__file__).resolve().parents[1] / 'Gurallar'))
if __name__ == '__main__':
    import runpy as programma_programma_paneli
    programma_programma_paneli.run_module('터미널글꼴빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('터미널글꼴빌드')
    대응 = {'data': 'maglumat', 'img': 'çyzgy_baha', 'bits': '비트들', 'x': 'x_koordinatasy', 'draw': '화면그리기', 'licences': '이용허락목록', 'paths': 'ýol_Sanaw', 'y': '세로좌표', 'main': 'Bitir', 'src': '원본주소', 'fonts': 'şrift_Sanaw', 'ROOT': '기준', 'p': '자료위치', 'cp': 'nyşan_kodlaşdyrma', 'target': 'niýet'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
