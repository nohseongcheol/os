#!/usr/bin/env python3
"""기존 Yoonu_jëmale 호환 dugal_xabaar_Tomb. liteew_mbir 구현: ../Jumtukaay_yi/예제빌드.py"""
import importlib as 가져오기
import sys as doxalukaay_xëyma
from pathlib import Path as Yoonu_jëmale
doxalukaay_xëyma.path.insert(0, str(Yoonu_jëmale(__file__).resolve().parents[1] / 'Jumtukaay_yi'))
if __name__ == '__main__':
    import runpy as jëfekaay_armuwaaru_jëfekaay
    jëfekaay_armuwaaru_jëfekaay.run_module('예제빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제빌드')
    대응 = {'out': '결과자료', 'build_examples': '예제만들기', 'files': 'bara_denc_lim', 'java': '자바실행', 'run': 'def_ndigel', 'path': 'Yoonu_jëmale', 'p': '자료위치', 'readme': 'JANG_MA', 'build_java_library': '자바라이브러리만들기', 'code': 'ndigal_SEQUENCE', 'index': '색인', 'classes': 'maas_Yoonu_jëmale', 'repo': '저장소경로', 'root': '뿌리주소', 'content': 'Këmb_xëyma', 'source': '원본자료', 'name': 'tur_253d1510', 'target': 'luñu_name', 'manifest': '꾸러미명세', 'language': 'Làkk'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
