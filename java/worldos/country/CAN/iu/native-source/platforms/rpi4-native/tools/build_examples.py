#!/usr/bin/env python3
"""기존 aqqut 호환 Iliniku_puinti. taannallarik_titiqqat 구현: ../도구/예제빌드.py"""
import importlib as 가져오기
import sys as qarasaujakkut_aulattijjut_atuutilik
from pathlib import Path as aqqut
qarasaujakkut_aulattijjut_atuutilik.path.insert(0, str(aqqut(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('예제빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제빌드')
    대응 = {'out': '결과자료', 'build_examples': '예제만들기', 'files': 'ini_Titiqpalliagaq', 'java': '자바실행', 'run': '실행', 'path': 'aqqut', 'p': '자료위치', 'readme': 'README', 'build_java_library': '자바라이브러리만들기', 'code': '명령열', 'index': '색인', 'classes': 'naliannuungavik_aqqut', 'repo': '저장소경로', 'root': '뿌리주소', 'content': 'Ilulingit_atuutilik', 'source': '원본자료', 'name': 'atiq', 'target': 'turaagaq', 'manifest': '꾸러미명세', 'language': 'pilirijjutinut_uqausiq'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
