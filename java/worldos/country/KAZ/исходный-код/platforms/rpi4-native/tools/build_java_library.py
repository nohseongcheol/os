#!/usr/bin/env python3
"""기존 путь 호환 точка_входа. фактический_данные реализация: ../инструменты/자바라이브러리빌드.py"""
import importlib as ВЗЯТЬ_ЗНАЧЕН
import sys as операционная_система_ЗНАЧЕН
from pathlib import Path as путь
операционная_система_ЗНАЧЕН.path.insert(0, str(путь(__file__).resolve().parents[1] / 'инструменты'))
if __name__ == '__main__':
    import runpy as программа_Launcher
    программа_Launcher.run_module('자바라이브러리빌드', run_name='__main__', alter_sys=True)
else:
    реализация = ВЗЯТЬ_ЗНАЧЕН.import_module('자바라이브러리빌드')
    сопоставление_ЗНАЧЕН = {'header': 'Заголовок_ЗНАЧЕН', 'sources': '원문목록', 'i': '순번', 'info': 'msinfo32_exe', 'payload': 'полезные_данные_данные', 'src': '원본주소', 'run': '실행', 'build_java_library': '자바라이브러리만들기', 'relative': 'относительный_путь', 'classes': 'Класс_путь', 'dist': 'распределение_путь', 'archive': 'Архив', 'output': 'выход', 'root': 'корень_АДРЕС', 'name': 'Название', 'jar': '자바꾸러미', 'b': 'СЕКУНДЫ_ЗНАЧЕН', 'entries': '항목들'}
    for Назад_товар, текущий_товар in сопоставление_ЗНАЧЕН.items():
        if hasattr(реализация, текущий_товар): globals()[Назад_товар] = getattr(реализация, текущий_товар)
