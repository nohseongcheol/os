#!/usr/bin/env python3
"""기존 путь 호환 точка_входа. фактический_данные реализация: ../инструменты/экспортировать_пакет_SDK.py"""
import importlib as ВЗЯТЬ_ЗНАЧЕН
import sys as операционная_система_ЗНАЧЕН
from pathlib import Path as путь
операционная_система_ЗНАЧЕН.path.insert(0, str(путь(__file__).resolve().parents[1] / 'инструменты'))
if __name__ == '__main__':
    import runpy as программа_Launcher
    программа_Launcher.run_module('экспортировать_пакет_SDK', run_name='__main__', alter_sys=True)
else:
    реализация = ВЗЯТЬ_ЗНАЧЕН.import_module('экспортировать_пакет_SDK')
    сопоставление_ЗНАЧЕН = {'out': 'KR_данные', 'obj': 'конечный_файл', 'relative': 'относительный_путь', 'compiler_archive': 'компилятор_Архив', 'sdk': 'комплект_SDK', 'dist': 'распределение_путь', 'archive': 'Архив', 'main': 'запустить', 'posix': '포직스경로', 'files': 'список_файлов', 'source': '원본자료', 'name': 'Название', 'target': 'целевое_значение', 'ROOT': 'задача_корень', 'destination': 'цель_данные_АДРЕС', 'manifest': 'пакет_манифест', 'work': '작업경로'}
    for Назад_товар, текущий_товар in сопоставление_ЗНАЧЕН.items():
        if hasattr(реализация, текущий_товар): globals()[Назад_товар] = getattr(реализация, текущий_товар)
