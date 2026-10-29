#!/usr/bin/env python3
"""기존 путь 호환 точка_входа. фактический_данные реализация: ../инструменты/BLD_пользователь_место.py"""
import importlib as ВЗЯТЬ_ЗНАЧЕН
import sys as операционная_система_ЗНАЧЕН
from pathlib import Path as путь
операционная_система_ЗНАЧЕН.path.insert(0, str(путь(__file__).resolve().parents[1] / 'инструменты'))
if __name__ == '__main__':
    import runpy as программа_Launcher
    программа_Launcher.run_module('BLD_пользователь_место', run_name='__main__', alter_sys=True)
else:
    реализация = ВЗЯТЬ_ЗНАЧЕН.import_module('BLD_пользователь_место')
    сопоставление_ЗНАЧЕН = {'mode': 'метод_МОДА', 'header': 'Заголовок_ЗНАЧЕН', 'i': '순번', 'build_ccompiler': 'Create_C_компилятор', 'ar': 'Архив_средство', 'posix': '포직스경로', 'payload': 'полезные_данные_данные', 'flags': 'настройки_BITS', 'cases': 'тестовый_случай', 'cc': 'C_компилятор', 'data': 'данные', 'build_java_library': '자바라이브러리만들기', 'ld': 'компоновщик_средство', 'repo': 'репозиторий_путь', 'build_python': 'Create_PYTHON', 'inc': 'включать_путь', 'argument': '전달값', 'text': 'текст', 'headers': 'Заголовок_Список', 'cxx': '시플플번역기', 'valid': 'допустимый', 'build': 'BLD', 'build_users': 'Create_пользователь_место', 'compiler': 'компилятор_средство', 'uzlib': '압축해제경로', 'extra': '추가영역', 'phoff': 'программа_Заголовок_СМЕЩ', 'offset': 'СМЕЩ_ЗНАЧЕН', 'text_address': '명령주소', 'abi': 'вызов_ABI', 'assembly': 'сборка_ec50080d', 'run': '실행', 'path': 'путь', 'p': 'данные_позиция', 'changed': '바뀐자료', 'n': 'товар_СЧЁТ', 'flag': 'Настройки_ЗНАЧЕН', 'index': 'Поиск_ИНДЕКС', 'classes': 'Класс_путь', 'output': 'выход', 'loads': '적재구획', 'data_address': 'данные_АДРЕС', 'symbol': 'символ_ЗНАЧЕН', 'root': 'корень_АДРЕС', 'patches': '수정사항', 'source': '원본자료', 'sizes': '크기목록', 'blobs': '탑재덩이들', 'name': 'Название', 'value': 'ЗНАЧЕН', 'fmt': 'формат_932e03c8', 'work': '작업경로'}
    for Назад_товар, текущий_товар in сопоставление_ЗНАЧЕН.items():
        if hasattr(реализация, текущий_товар): globals()[Назад_товар] = getattr(реализация, текущий_товар)
