#!/usr/bin/env python3
"""기존 пут 호환 унос_тачка. стваран_подаци 구현: ../도구/자바라이브러리빌드.py"""
import importlib as 가져오기
import sys as оперативни_систем_вриједност
from pathlib import Path as пут
оперативни_систем_вриједност.path.insert(0, str(пут(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('자바라이브러리빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('자바라이브러리빌드')
    대응 = {'header': 'заглавље_вриједност', 'sources': '원문목록', 'i': '순번', 'info': 'систем_информација', 'payload': 'корисни_садржај_подаци', 'src': '원본주소', 'run': '실행', 'build_java_library': '자바라이브러리만들기', 'relative': '상대경로', 'classes': 'класа_пут', 'dist': '배포경로', 'archive': 'архива', 'output': '출력결과', 'root': '뿌리주소', 'name': 'назив', 'jar': '자바꾸러미', 'b': '둘째값', 'entries': '항목들'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
