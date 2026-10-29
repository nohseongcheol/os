#!/usr/bin/env python3
"""기존 пут 호환 унос_тачка. стваран_подаци 구현: ../도구/개발꾸러미번역.py"""
import importlib as 가져오기
import sys as оперативни_систем_вриједност
from pathlib import Path as пут
оперативни_систем_вриједност.path.insert(0, str(пут(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('개발꾸러미번역', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('개발꾸러미번역')
    대응 = {'compiler': '번역기', 'obj': 'одредишни_фајл', 'sdk': '개발꾸러미', 'output': '출력결과', 'main': '시작', 'elf': '실행파일', 'is_c': '시언어여부', 'parser': '인수해석기', 'language': 'Језик', 'work': '작업경로', 'args': 'аргумент_низ'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
