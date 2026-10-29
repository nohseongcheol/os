#!/usr/bin/env python3
"""기존 Yul 호환 кертү_балл. фактик_мәгълүмат 구현: ../Кораллар/예제빌드.py"""
import importlib as TAKE_VALUE
import sys as операцион_система_VALUE
from pathlib import Path as Yul
операцион_система_VALUE.path.insert(0, str(Yul(__file__).resolve().parents[1] / 'Кораллар'))
if __name__ == '__main__':
    import runpy as кушымта_хезмәткәр
    кушымта_хезмәткәр.run_module('예제빌드', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('예제빌드')
    대응 = {'out': 'үлчәм_мәгълүмат', 'build_examples': '예제만들기', 'files': 'файл_Исемлек', 'java': '자바실행', 'run': 'үтәргә_команда', 'path': 'Yul', 'p': 'мәгълүмат_урнаштыру', 'readme': 'Белешмә_файлы', 'build_java_library': '자바라이브러리만들기', 'code': 'инструкция_SEQUENCE', 'index': 'Эзләү_INDEX', 'classes': 'класс_юл', 'repo': '저장소경로', 'root': 'тамыр_адрес', 'content': 'Эчтәлек_VALUE', 'source': '원본자료', 'name': 'исем', 'target': 'максат_кыйммәт', 'manifest': '꾸러미명세', 'language': 'тел'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
