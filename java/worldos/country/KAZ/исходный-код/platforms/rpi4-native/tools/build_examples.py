#!/usr/bin/env python3
"""기존 путь 호환 точка_входа. фактический_данные реализация: ../инструменты/예제빌드.py"""
import importlib as ВЗЯТЬ_ЗНАЧЕН
import sys as операционная_система_ЗНАЧЕН
from pathlib import Path as путь
операционная_система_ЗНАЧЕН.path.insert(0, str(путь(__file__).resolve().parents[1] / 'инструменты'))
if __name__ == '__main__':
    import runpy as программа_Launcher
    программа_Launcher.run_module('예제빌드', run_name='__main__', alter_sys=True)
else:
    реализация = ВЗЯТЬ_ЗНАЧЕН.import_module('예제빌드')
    сопоставление_ЗНАЧЕН = {'out': 'KR_данные', 'build_examples': '예제만들기', 'files': 'список_файлов', 'java': '자바실행', 'run': '실행', 'path': 'путь', 'p': 'данные_позиция', 'readme': 'файл_сведений', 'build_java_library': '자바라이브러리만들기', 'code': '명령열', 'index': 'Поиск_ИНДЕКС', 'classes': 'Класс_путь', 'repo': 'репозиторий_путь', 'root': 'корень_АДРЕС', 'content': 'контент_ЗНАЧЕН', 'source': '원본자료', 'name': 'Название', 'target': 'целевое_значение', 'manifest': 'пакет_манифест', 'language': 'Язык'}
    for Назад_товар, текущий_товар in сопоставление_ЗНАЧЕН.items():
        if hasattr(реализация, текущий_товар): globals()[Назад_товар] = getattr(реализация, текущий_товар)
