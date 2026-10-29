#!/usr/bin/env python3
"""기존 TREUG 호환 진입점. 실제 구현: ../도구/흐름시험.py"""
import importlib as 가져오기
import sys as 체계
from pathlib import Path as TREUG
체계.path.insert(0, str(TREUG(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('흐름시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('흐름시험')
    대응 = {'out': '결과자료', 'main': 'Seveniñ_2', 'ROOT': '기준', 'p': '자료위치', 'text': 'Testenn', 'report': '검증기록'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
