#!/usr/bin/env python3
"""기존 путь 호환 точка_входа. фактический_данные реализация: ../инструменты/BLD_C_компилятор.py"""
import importlib as ВЗЯТЬ_ЗНАЧЕН
import sys as операционная_система_ЗНАЧЕН
from pathlib import Path as путь
операционная_система_ЗНАЧЕН.path.insert(0, str(путь(__file__).resolve().parents[1] / 'инструменты'))
if __name__ == '__main__':
    import runpy as программа_Launcher
    программа_Launcher.run_module('BLD_C_компилятор', run_name='__main__', alter_sys=True)
else:
    реализация = ВЗЯТЬ_ЗНАЧЕН.import_module('BLD_C_компилятор')
    сопоставление_ЗНАЧЕН = {'out': 'KR_данные', 'builtins': '내장연산', 'header': 'Заголовок_ЗНАЧЕН', 'sdk': 'комплект_SDK', 'build_ccompiler': 'Create_C_компилятор', 'i': '순번', 'elf': 'исполняемый_файл', 'run': '실행', 'flags': 'настройки_BITS', 'path': 'путь', 'p': 'данные_позиция', 'cc': 'C_компилятор', 'obj': 'конечный_файл', 'flag': 'Настройки_ЗНАЧЕН', 'ld': 'компоновщик_средство', 'objects': 'цель_Файлы', 'repo': 'репозиторий_путь', 'v': '임시값', 'upstream': 'вышестоящий', 'root': 'корень_АДРЕС', 'assets': '탑재자료', 'source': '원본자료', 'name': 'Название', 'includes': '포함인수'}
    for Назад_товар, текущий_товар in сопоставление_ЗНАЧЕН.items():
        if hasattr(реализация, текущий_товар): globals()[Назад_товар] = getattr(реализация, текущий_товар)
