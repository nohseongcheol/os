#!/usr/bin/env python3
"""기존 путь 호환 точка_входа. фактический_данные реализация: ../инструменты/сборка.py"""
import importlib as ВЗЯТЬ_ЗНАЧЕН
import sys as операционная_система_ЗНАЧЕН
from pathlib import Path as путь
операционная_система_ЗНАЧЕН.path.insert(0, str(путь(__file__).resolve().parents[1] / 'инструменты'))
if __name__ == '__main__':
    import runpy as программа_Launcher
    программа_Launcher.run_module('сборка', run_name='__main__', alter_sys=True)
else:
    реализация = ВЗЯТЬ_ЗНАЧЕН.import_module('сборка')
    сопоставление_ЗНАЧЕН = {'network': 'сеть', 'BUILD': 'BLD_путь', 'ar': 'Архив_средство', 'build_examples': '예제만들기', 'posix': '포직스경로', 'font_data': 'шрифт_данные', 'flags': 'настройки_BITS', 'a': '첫째값', 'cc': 'C_компилятор', 'args': 'аргумент_МАССИВ', 'source_flags': '원본설정', 'ld': 'компоновщик_средство', 'method': 'метод_ввод', 'main': 'запустить', 'objcopy': 'объектный_файл_преобразователь', 'ROOT': 'задача_корень', 'cxx': '시플플번역기', 'includes': '포함인수', 'compiler': 'компилятор_средство', 'build_users': 'Create_пользователь_место', 'f': 'файл_ввод', 'extra': '추가영역', 'exports': 'экспортировать_таблица', 'jobs': '빌드작업', 'run': '실행', 'path': 'путь', 'REPO': 'корень_репозитория', 'tool': 'инструменты', 'classes': 'Класс_путь', 'output': 'выход', 'samples': '예제들', 'symbol': 'символ_ЗНАЧЕН', 'source': '원본자료', 'name': 'Название', 'build_network': 'Create_сеть', 'font_info': 'шрифт_сведения', 'manifest': 'пакет_манифест', 'work': '작업경로'}
    for Назад_товар, текущий_товар in сопоставление_ЗНАЧЕН.items():
        if hasattr(реализация, текущий_товар): globals()[Назад_товар] = getattr(реализация, текущий_товар)
