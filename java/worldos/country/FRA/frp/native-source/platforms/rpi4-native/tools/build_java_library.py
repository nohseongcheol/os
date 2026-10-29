#!/usr/bin/env python3
"""기존 경로 호환 진입점. 실제 구현: ../도구/자바라이브러리빌드.py"""
import importlib as 가져오기
import sys as 체계
from pathlib import Path as 경로
체계.path.insert(0, str(경로(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('자바라이브러리빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('자바라이브러리빌드')
    대응 = {'header': '머리부', 'sources': '원문목록', 'i': '순번', 'info': '정보', 'payload': '내용자료', 'src': '원본주소', 'run': '실행', 'build_java_library': '자바라이브러리만들기', 'relative': '상대경로', 'classes': '클래스경로', 'dist': '배포경로', 'archive': '압축꾸러미', 'output': '출력결과', 'root': '뿌리주소', 'name': 'Nom', 'jar': '자바꾸러미', 'b': '둘째값', 'entries': '항목들'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
