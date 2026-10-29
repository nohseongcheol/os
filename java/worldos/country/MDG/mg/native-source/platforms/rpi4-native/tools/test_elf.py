#!/usr/bin/env python3
"""기존 LALANA 호환 진입점. 실제 구현: ../도구/실행파일시험.py"""
import importlib as 가져오기
import sys as 체계
from pathlib import Path as LALANA
체계.path.insert(0, str(LALANA(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('실행파일시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('실행파일시험')
    대응 = {'out': '결과자료', 'expected': '예상결과', 'phoff': '프로그램머리변위', 'offset': '변위', 'invalid': '잘못된자료', 'path': 'LALANA', 'executable': '실행가능파일', 'rejected': '거부결과', 'linux_example': '리눅스예제', 'original': '원본', 'result': '결과', 'format_': '형식지정', 'main': 'Alefaso', 'content': '내용', 'source': '원본자료', 'name': 'Anarana', 'reference': '비교기준', 'ROOT': '기준', 'value': '값', 'report': '검증기록'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
