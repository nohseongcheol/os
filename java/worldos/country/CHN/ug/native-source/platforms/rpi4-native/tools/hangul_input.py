#!/usr/bin/env python3
"""기존 يول 호환 كىرگۈزۈش_نوقتا. ھەقىقىي_مەلۇمات 구현: ../قوراللار/한글입력.py"""
import importlib as 가져오기
import sys as مەشغۇلات_سىستېمىسى_قىممىتى
from pathlib import Path as يول
مەشغۇلات_سىستېمىسى_قىممىتى.path.insert(0, str(يول(__file__).resolve().parents[1] / 'قوراللار'))
if __name__ == '__main__':
    import runpy as ئەپ_خادىم
    ئەپ_خادىم.run_module('한글입력', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('한글입력')
    대응 = {'old': '이전', 'backspace': '앞글자지우기', 'committed': '확정글', 'KEYS': 'ئاچقۇچ_لايىھە', 'self': '자신', 'FINALS': '겹끝소리', 'VOWELS': '겹가운뎃소리', 'INITIAL': '첫소리목록', 'initial': '첫소리', 'commit': '조합확정', 'feed': 'ئۇچۇر_ئاچقۇچ', 'vowel': '가운뎃소리', 'Hangul': '한글조합', 'SPLIT': '끝소리가르기', 'final': '끝소리', 'key': '누름값', 'send': 'ئەۋەتمەك', 'left': '왼쪽', 'FINAL': '끝소리목록', 'history': 'تارىخ', 'pair': '한쌍', 'char': 'ھەرپ_بەلگە_مەلۇمات', 'VOWEL': '가운뎃소리목록', 'right': '오른쪽', 'value': 'قىممىتى', 'text': 'تېكىست'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
