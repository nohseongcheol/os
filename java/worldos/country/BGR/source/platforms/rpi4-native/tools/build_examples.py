#!/usr/bin/env python3
"""기존 ПЪТ 호환 запис_пункт. действителен_данни 구현: ../Инструменти/예제빌드.py"""
import importlib as 가져오기
import sys as операционна_система_стойност
from pathlib import Path as ПЪТ
операционна_система_стойност.path.insert(0, str(ПЪТ(__file__).resolve().parents[1] / 'Инструменти'))
if __name__ == '__main__':
    import runpy as програма_програма_за_стартиране
    програма_програма_за_стартиране.run_module('예제빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제빌드')
    съпоставяне_стойност = {'out': 'мярка_данни', 'build_examples': '예제만들기', 'files': 'Файл_Списък', 'java': '자바실행', 'run': 'изпълнявам_команда', 'path': 'ПЪТ', 'p': 'данни_позиция', 'readme': '안내자료', 'build_java_library': '자바라이브러리만들기', 'code': '명령열', 'index': 'Търсене_индекс', 'classes': 'Клас_път', 'repo': 'хранилище_път', 'root': 'корен_адрес', 'content': 'Съдържание_стойност', 'source': '원본자료', 'name': 'Име', 'target': 'цел', 'manifest': 'пакет_манифест', 'language': 'език'}
    for 이전, в_срок_артикул in съпоставяне_стойност.items():
        if hasattr(구현, в_срок_артикул): globals()[이전] = getattr(구현, в_срок_артикул)
