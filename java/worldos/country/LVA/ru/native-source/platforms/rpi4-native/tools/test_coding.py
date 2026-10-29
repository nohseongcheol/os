#!/usr/bin/env python3
"""기존 путь 호환 точка_входа. фактический_данные реализация: ../инструменты/코딩시험.py"""
import importlib as ВЗЯТЬ_ЗНАЧЕН
import sys as операционная_система_ЗНАЧЕН
from pathlib import Path as путь
операционная_система_ЗНАЧЕН.path.insert(0, str(путь(__file__).resolve().parents[1] / 'инструменты'))
if __name__ == '__main__':
    import runpy as программа_Launcher
    программа_Launcher.run_module('코딩시험', run_name='__main__', alter_sys=True)
else:
    реализация = ВЗЯТЬ_ЗНАЧЕН.import_module('코딩시험')
    сопоставление_ЗНАЧЕН = {'out': 'KR_данные', 'expected': '예상결과', 'sdk': 'комплект_SDK', 'suffix': '뒷부분', 'arc': '압축묶음', 'main': 'запустить', 'elf': 'исполняемый_файл', 'run': '실행', 'name': 'Название', 'path': 'путь', 'p': 'данные_позиция', 'ROOT': 'задача_корень', 'report': 'проверка_Отчет', 'args': 'аргумент_МАССИВ'}
    for Назад_товар, текущий_товар in сопоставление_ЗНАЧЕН.items():
        if hasattr(реализация, текущий_товар): globals()[Назад_товар] = getattr(реализация, текущий_товар)
