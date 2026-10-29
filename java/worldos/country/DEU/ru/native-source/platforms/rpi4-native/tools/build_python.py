#!/usr/bin/env python3
"""기존 путь 호환 точка_входа. фактический_данные реализация: ../инструменты/BLD_PYTHON.py"""
import importlib as ВЗЯТЬ_ЗНАЧЕН
import sys as операционная_система_ЗНАЧЕН
from pathlib import Path as путь
операционная_система_ЗНАЧЕН.path.insert(0, str(путь(__file__).resolve().parents[1] / 'инструменты'))
if __name__ == '__main__':
    import runpy as программа_Launcher
    программа_Launcher.run_module('BLD_PYTHON', run_name='__main__', alter_sys=True)
else:
    реализация = ВЗЯТЬ_ЗНАЧЕН.import_module('BLD_PYTHON')
    сопоставление_ЗНАЧЕН = {'ld': 'компоновщик_средство', 'archive': 'Архив', 'SHA256': 'проверка_хэш', 'build_python': 'Create_PYTHON', 'root': 'корень_АДРЕС', 'source': '원본자료', 'name': 'Название', 'path': 'путь', 'VERSION': 'выпуск_ЗНАЧЕН_237a4c94', 'cc': 'C_компилятор', 'tar': 'TAR_пакет', 'newlib': '뉴리브포함경로', 'member': 'член'}
    for Назад_товар, текущий_товар in сопоставление_ЗНАЧЕН.items():
        if hasattr(реализация, текущий_товар): globals()[Назад_товар] = getattr(реализация, текущий_товар)
