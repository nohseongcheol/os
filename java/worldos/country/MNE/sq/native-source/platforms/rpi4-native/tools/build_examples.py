#!/usr/bin/env python3
"""기존 POZICIONI 호환 futje_p. aktual_të_dhëna 구현: ../Mjete/예제빌드.py"""
import importlib as TAKE_VALUE
import sys as sistem_operativ_VALUE
from pathlib import Path as POZICIONI
sistem_operativ_VALUE.path.insert(0, str(POZICIONI(__file__).resolve().parents[1] / 'Mjete'))
if __name__ == '__main__':
    import runpy as program_hapës
    program_hapës.run_module('예제빌드', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('예제빌드')
    대응 = {'out': 'llogaritje_të_dhëna', 'build_examples': '예제만들기', 'files': 'skedar_Listë', 'java': '자바실행', 'run': 'zbatoj_komandë', 'path': 'POZICIONI', 'p': 'të_dhëna_pozicioni', 'readme': 'LEXOMË', 'build_java_library': '자바라이브러리만들기', 'code': 'instruksion_SEQUENCE', 'index': 'LOOKUP_INDEX', 'classes': 'klasë_shteg', 'repo': 'depo_shteg', 'root': 'rrënjë_email', 'content': 'Përmbajtje_VALUE', 'source': '원본자료', 'name': 'Emër', 'target': 'objektiv', 'manifest': '꾸러미명세', 'language': 'Gjuha'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
