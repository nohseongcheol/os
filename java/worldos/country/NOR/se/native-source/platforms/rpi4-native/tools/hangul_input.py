#!/usr/bin/env python3
"""기존 경로 호환 진입점. 실제 구현: ../도구/한글입력.py"""
import importlib as 가져오기
import sys as 체계
from pathlib import Path as 경로
체계.path.insert(0, str(경로(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('한글입력', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('한글입력')
    대응 = {'old': '이전', 'backspace': '앞글자지우기', 'committed': '확정글', 'KEYS': '글쇠배열', 'self': '자신', 'FINALS': '겹끝소리', 'VOWELS': '겹가운뎃소리', 'INITIAL': '첫소리목록', 'initial': '첫소리', 'commit': '조합확정', 'feed': '글쇠넣기', 'vowel': '가운뎃소리', 'Hangul': '한글조합', 'SPLIT': '끝소리가르기', 'final': '끝소리', 'key': '누름값', 'send': '보내기', 'left': '왼쪽', 'FINAL': '끝소리목록', 'history': '지난기록', 'pair': '한쌍', 'char': '글자값', 'VOWEL': '가운뎃소리목록', 'right': '오른쪽', 'value': '값', 'text': 'teaksta'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
