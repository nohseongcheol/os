#!/usr/bin/env python3
"""기존 경로 호환 진입점. 실제 구현: ../도구/자바가상기계시험.py"""
import importlib as 가져오기
import sys as 체계
from pathlib import Path as 경로
체계.path.insert(0, str(경로(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('자바가상기계시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('자바가상기계시험')
    대응 = {'message': '알림문', 's': '문자열값', 'actual': '실제결과', 'match': '일치', 'payload': '내용자료', 'cases': '시험사례', 'fixture': '시험자료', 'main': 'Tandika', 'ROOT': '기준', 'text': 'Bigambo', 'valid': '유효함', 'includes': '포함인수', 'include': '포함항목', 'expected': '예상결과', 'sources': '원문목록', 'tmp': '임시경로', 'done': '완료량', 'classes': '클래스경로', 'output': '출력결과', 'result': 'KIGENDERWA', 'cmd': '명령인수', 'name': 'Linnya', 'jar': '자바꾸러미', 'report': '검증기록', 'tests': '시험목록'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
