#!/usr/bin/env python3
"""기존 Ýol 호환 girizmeklik_utuk. hakyky_maglumat 구현: ../Gurallar/예제빌드.py"""
import importlib as 가져오기
import sys as operasiýa_ulgamy_baha
from pathlib import Path as Ýol
operasiýa_ulgamy_baha.path.insert(0, str(Ýol(__file__).resolve().parents[1] / 'Gurallar'))
if __name__ == '__main__':
    import runpy as programma_programma_paneli
    programma_programma_paneli.run_module('예제빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제빌드')
    대응 = {'out': '결과자료', 'build_examples': '예제만들기', 'files': 'faýl_Sanaw', 'java': '자바실행', 'run': 'ýerine_ýetir_buýruk', 'path': 'Ýol', 'p': '자료위치', 'readme': 'README', 'build_java_library': '자바라이브러리만들기', 'code': 'instruksiýa_SEQUENCE', 'index': '색인', 'classes': 'klas_ýol', 'repo': '저장소경로', 'root': '뿌리주소', 'content': 'Mazmun_baha', 'source': '원본자료', 'name': 'Ad', 'target': 'niýet', 'manifest': '꾸러미명세', 'language': 'Dil'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
