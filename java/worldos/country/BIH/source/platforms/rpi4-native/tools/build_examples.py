#!/usr/bin/env python3
"""기존 пут 호환 унос_тачка. стваран_подаци 구현: ../도구/예제빌드.py"""
import importlib as 가져오기
import sys as оперативни_систем_вриједност
from pathlib import Path as пут
оперативни_систем_вриједност.path.insert(0, str(пут(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('예제빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제빌드')
    대응 = {'out': '결과자료', 'build_examples': '예제만들기', 'files': 'фајл_списак', 'java': '자바실행', 'run': '실행', 'path': 'пут', 'p': '자료위치', 'readme': 'Прочитај_ме', 'build_java_library': '자바라이브러리만들기', 'code': '명령열', 'index': '색인', 'classes': 'класа_пут', 'repo': '저장소경로', 'root': '뿌리주소', 'content': 'Садржај_вриједност', 'source': '원본자료', 'name': 'назив', 'target': 'циљ', 'manifest': '꾸러미명세', 'language': 'Језик'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
