#!/usr/bin/env python3
"""기존 ПЪТ 호환 запис_пункт. действителен_данни 구현: ../Инструменти/자바라이브러리빌드.py"""
import importlib as 가져오기
import sys as операционна_система_стойност
from pathlib import Path as ПЪТ
операционна_система_стойност.path.insert(0, str(ПЪТ(__file__).resolve().parents[1] / 'Инструменти'))
if __name__ == '__main__':
    import runpy as програма_програма_за_стартиране
    програма_програма_за_стартиране.run_module('자바라이브러리빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('자바라이브러리빌드')
    съпоставяне_стойност = {'header': 'Заглавка_стойност', 'sources': '원문목록', 'i': '순번', 'info': 'Системна_информация', 'payload': 'полезен_обем_данни', 'src': '원본주소', 'run': 'изпълнявам_команда', 'build_java_library': '자바라이브러리만들기', 'relative': 'относителен_път', 'classes': 'Клас_път', 'dist': '배포경로', 'archive': 'Архив', 'output': '출력결과', 'root': 'корен_адрес', 'name': 'Име', 'jar': '자바꾸러미', 'b': '둘째값', 'entries': '항목들'}
    for 이전, в_срок_артикул in съпоставяне_стойност.items():
        if hasattr(구현, в_срок_артикул): globals()[이전] = getattr(구현, в_срок_артикул)
