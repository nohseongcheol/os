#!/usr/bin/env python3
"""기존 ПЪТ 호환 запис_пункт. действителен_данни 구현: ../Инструменти/한글입력.py"""
import importlib as 가져오기
import sys as операционна_система_стойност
from pathlib import Path as ПЪТ
операционна_система_стойност.path.insert(0, str(ПЪТ(__file__).resolve().parents[1] / 'Инструменти'))
if __name__ == '__main__':
    import runpy as програма_програма_за_стартиране
    програма_програма_за_стартиране.run_module('한글입력', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('한글입력')
    съпоставяне_стойност = {'old': '이전', 'backspace': '앞글자지우기', 'committed': '확정글', 'KEYS': 'Ключ_схема', 'self': '자신', 'FINALS': '겹끝소리', 'VOWELS': '겹가운뎃소리', 'INITIAL': '첫소리목록', 'initial': '첫소리', 'commit': '조합확정', 'feed': 'поток_Ключ', 'vowel': '가운뎃소리', 'Hangul': '한글조합', 'SPLIT': '끝소리가르기', 'final': '끝소리', 'key': '누름값', 'send': 'изпращам', 'left': '왼쪽', 'FINAL': '끝소리목록', 'history': 'Хронология', 'pair': '한쌍', 'char': 'знакови_данни', 'VOWEL': '가운뎃소리목록', 'right': '오른쪽', 'value': 'стойност', 'text': 'Текст'}
    for 이전, в_срок_артикул in съпоставяне_стойност.items():
        if hasattr(구현, в_срок_артикул): globals()[이전] = getattr(구현, в_срок_артикул)
