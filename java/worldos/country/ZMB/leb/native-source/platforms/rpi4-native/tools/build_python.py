#!/usr/bin/env python3
"""기존 경로 호환 진입점. 실제 구현: ../도구/파이썬빌드.py"""
import importlib as 가져오기
import sys as 체계
from pathlib import Path as 경로
체계.path.insert(0, str(경로(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('파이썬빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('파이썬빌드')
    대응 = {'ld': '연결편집기', 'archive': '압축꾸러미', 'SHA256': '검증해시', 'build_python': '파이썬만들기', 'root': '뿌리주소', 'source': '원본자료', 'name': '이름', 'path': '경로', 'VERSION': '배포판', 'cc': '시언어번역기', 'tar': '타르꾸러미', 'newlib': '뉴리브포함경로', 'member': '구성원'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
