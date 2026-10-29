#!/usr/bin/env python3
"""기존 путь 호환 точка_входа. фактический_данные реализация: ../инструменты/실행.py"""
import importlib as ВЗЯТЬ_ЗНАЧЕН
import sys as операционная_система_ЗНАЧЕН
from pathlib import Path as путь
операционная_система_ЗНАЧЕН.path.insert(0, str(путь(__file__).resolve().parents[1] / 'инструменты'))
if __name__ == '__main__':
    import runpy as программа_Launcher
    программа_Launcher.run_module('실행', run_name='__main__', alter_sys=True)
else:
    реализация = ВЗЯТЬ_ЗНАЧЕН.import_module('실행')
    сопоставление_ЗНАЧЕН = {'supported': '지원목록', 'parser': 'анализатор', 'qemu': '모의기계', 'run_desktop': 'выполнить_компьютер', 'main': 'запустить', 'host': 'узел', 'status': 'Состояние_ЗНАЧЕН', 'NetworkBridge': 'мост_3de4fe3a', 'ROOT': 'задача_корень', 'bridge': 'мост', 'loader': 'загрузчик', 'base': 'фон_ЗНАЧЕН', 'options': 'Параметры', 'binary': 'binary', 'args': 'аргумент_МАССИВ', 'command': 'команда'}
    for Назад_товар, текущий_товар in сопоставление_ЗНАЧЕН.items():
        if hasattr(реализация, текущий_товар): globals()[Назад_товар] = getattr(реализация, текущий_товар)
