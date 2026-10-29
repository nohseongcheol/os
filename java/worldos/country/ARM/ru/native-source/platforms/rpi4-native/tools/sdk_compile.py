#!/usr/bin/env python3
"""기존 путь 호환 точка_входа. фактический_данные реализация: ../инструменты/пакет_SDK_компилировать.py"""
import importlib as ВЗЯТЬ_ЗНАЧЕН
import sys as операционная_система_ЗНАЧЕН
from pathlib import Path as путь
операционная_система_ЗНАЧЕН.path.insert(0, str(путь(__file__).resolve().parents[1] / 'инструменты'))
if __name__ == '__main__':
    import runpy as программа_Launcher
    программа_Launcher.run_module('пакет_SDK_компилировать', run_name='__main__', alter_sys=True)
else:
    реализация = ВЗЯТЬ_ЗНАЧЕН.import_module('пакет_SDK_компилировать')
    сопоставление_ЗНАЧЕН = {'compiler': 'компилятор_средство', 'obj': 'конечный_файл', 'sdk': 'комплект_SDK', 'output': 'выход', 'main': 'запустить', 'elf': 'исполняемый_файл', 'is_c': 'ИТ_службы_C_Язык', 'parser': 'анализатор', 'language': 'Язык', 'work': '작업경로', 'args': 'аргумент_МАССИВ'}
    for Назад_товар, текущий_товар in сопоставление_ЗНАЧЕН.items():
        if hasattr(реализация, текущий_товар): globals()[Назад_товар] = getattr(реализация, текущий_товар)
