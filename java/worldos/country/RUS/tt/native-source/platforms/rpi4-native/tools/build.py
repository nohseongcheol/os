#!/usr/bin/env python3
"""기존 Yul 호환 кертү_балл. фактик_мәгълүмат 구현: ../Кораллар/төзү_система.py"""
import importlib as TAKE_VALUE
import sys as операцион_система_VALUE
from pathlib import Path as Yul
операцион_система_VALUE.path.insert(0, str(Yul(__file__).resolve().parents[1] / 'Кораллар'))
if __name__ == '__main__':
    import runpy as кушымта_хезмәткәр
    кушымта_хезмәткәр.run_module('төзү_система', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('төзү_система')
    대응 = {'network': 'Челтәр', 'BUILD': 'төзү_юл', 'ar': 'Архив_чара', 'build_examples': '예제만들기', 'posix': '포직스경로', 'font_data': 'шрифт_мәгълүмат', 'flags': '설정비트', 'a': '첫째값', 'cc': '시언어번역기', 'args': 'аргумент_МАССИВ', 'source_flags': '원본설정', 'ld': '연결편집기', 'method': 'ысул_кертү', 'main': 'эшләтү', 'objcopy': 'объект_файл_конвертер', 'ROOT': 'экранга_җибәрү_тамыр', 'cxx': '시플플번역기', 'includes': '포함인수', 'compiler': '번역기', 'build_users': 'Төзү_кулланучы_өлкә', 'f': 'файл_кертү', 'extra': '추가영역', 'exports': 'экспортлау_таблица', 'jobs': '빌드작업', 'run': 'үтәргә_команда', 'path': 'Yul', 'REPO': '저장소', 'tool': 'Кораллар', 'classes': 'класс_юл', 'output': '출력결과', 'samples': '예제들', 'symbol': 'символ_VALUE', 'source': '원본자료', 'name': 'исем', 'build_network': 'Төзү_Челтәр', 'font_info': 'шрифт_мәгълүмат_c16c0f1c', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
