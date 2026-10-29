#!/usr/bin/env python3
"""기존 Yoonu_jëmale 호환 dugal_xabaar_Tomb. liteew_mbir 구현: ../Jumtukaay_yi/터미널글꼴빌드.py"""
import importlib as 가져오기
import sys as doxalukaay_xëyma
from pathlib import Path as Yoonu_jëmale
doxalukaay_xëyma.path.insert(0, str(Yoonu_jëmale(__file__).resolve().parents[1] / 'Jumtukaay_yi'))
if __name__ == '__main__':
    import runpy as jëfekaay_armuwaaru_jëfekaay
    jëfekaay_armuwaaru_jëfekaay.run_module('터미널글꼴빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('터미널글꼴빌드')
    대응 = {'data': 'mbir', 'img': 'deseñ_xëyma', 'bits': '비트들', 'x': 'rëddu_iks_yi', 'draw': '화면그리기', 'licences': '이용허락목록', 'paths': 'Yoonu_jëmale_lim', 'y': '세로좌표', 'main': 'daw', 'src': '원본주소', 'fonts': 'mbindin_lim', 'ROOT': '기준', 'p': '자료위치', 'cp': 'Araf_nëbbin_ci_lim', 'target': 'luñu_name'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
