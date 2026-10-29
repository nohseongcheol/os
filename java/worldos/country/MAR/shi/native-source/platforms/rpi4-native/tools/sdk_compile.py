#!/usr/bin/env python3
"""기존 경로 호환 진입점. 실제 구현: ../도구/개발꾸러미번역.py"""
import importlib as 가져오기
import sys as 체계
from pathlib import Path as 경로
체계.path.insert(0, str(경로(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('개발꾸러미번역', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('개발꾸러미번역')
    대응 = {'compiler': '번역기', 'obj': '목적파일', 'sdk': '개발꾸러미', 'output': '출력결과', 'main': '시작', 'elf': '실행파일', 'is_c': '시언어여부', 'parser': '인수해석기', 'language': '언어', 'work': '작업경로', 'args': '인수배열'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
