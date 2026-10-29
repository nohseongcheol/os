#!/usr/bin/env python3
"""기존 ПЪТ 호환 запис_пункт. действителен_данни 구현: ../Инструменти/изпълнявам_команда.py"""
import importlib as 가져오기
import sys as операционна_система_стойност
from pathlib import Path as ПЪТ
операционна_система_стойност.path.insert(0, str(ПЪТ(__file__).resolve().parents[1] / 'Инструменти'))
if __name__ == '__main__':
    import runpy as програма_програма_за_стартиране
    програма_програма_за_стартиране.run_module('изпълнявам_команда', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('изпълнявам_команда')
    съпоставяне_стойност = {'supported': '지원목록', 'parser': 'анализатор', 'qemu': '모의기계', 'run_desktop': 'изпълнение_десктоп', 'main': 'Стартиране', 'host': 'хост', 'status': 'Състояние_стойност', 'NetworkBridge': 'мост_3de4fe3a', 'ROOT': 'проект_корен', 'bridge': 'мост', 'loader': 'зареждаща_служебна_програма', 'base': 'Фон_стойност', 'options': 'Опции', 'binary': 'двоичен', 'args': 'аргумент_масив', 'command': 'Команда'}
    for 이전, в_срок_артикул in съпоставяне_стойност.items():
        if hasattr(구현, в_срок_артикул): globals()[이전] = getattr(구현, в_срок_артикул)
