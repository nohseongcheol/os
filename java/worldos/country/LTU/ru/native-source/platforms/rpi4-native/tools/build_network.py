#!/usr/bin/env python3
"""기존 путь 호환 точка_входа. фактический_данные реализация: ../инструменты/BLD_сеть.py"""
import importlib as ВЗЯТЬ_ЗНАЧЕН
import sys as операционная_система_ЗНАЧЕН
from pathlib import Path as путь
операционная_система_ЗНАЧЕН.path.insert(0, str(путь(__file__).resolve().parents[1] / 'инструменты'))
if __name__ == '__main__':
    import runpy as программа_Launcher
    программа_Launcher.run_module('BLD_сеть', run_name='__main__', alter_sys=True)
else:
    реализация = ВЗЯТЬ_ЗНАЧЕН.import_module('BLD_сеть')
    сопоставление_ЗНАЧЕН = {'obj': 'конечный_файл', 'objects': 'цель_Файлы', 'library': 'библиотека', 'output': 'выход', 'port': 'номер_порта', 'root': 'корень_АДРЕС', 'files': 'список_файлов', 'source': '원본자료', 'run': '실행', 'flags': 'настройки_BITS', 'path': 'путь', 'build_network': 'Create_сеть', 'cc': 'C_компилятор', 'ar': 'Архив_средство'}
    for Назад_товар, текущий_товар in сопоставление_ЗНАЧЕН.items():
        if hasattr(реализация, текущий_товар): globals()[Назад_товар] = getattr(реализация, текущий_товар)
