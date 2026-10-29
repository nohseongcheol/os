#!/usr/bin/env python3
"""기존 шлях 호환 запис_бал. фактично_дані реалізація: ../інструменти/Виконати_команда.py"""
import importlib as 가져오기
import sys as операційна_система_ОС_значення
from pathlib import Path as шлях
операційна_система_ОС_значення.path.insert(0, str(шлях(__file__).resolve().parents[1] / 'інструменти'))
if __name__ == '__main__':
    import runpy as програма_запускач
    програма_запускач.run_module('Виконати_команда', run_name='__main__', alter_sys=True)
else:
    реалізація = 가져오기.import_module('Виконати_команда')
    зіставлення_значення = {'supported': '지원목록', 'parser': 'аналізатор', 'qemu': '모의기계', 'run_desktop': 'запускати_настільний', 'main': 'запустити', 'host': 'хост', 'status': 'Стан_значення', 'NetworkBridge': 'міст_3de4fe3a', 'ROOT': 'Дії_корінь', 'bridge': 'міст', 'loader': 'завантажувач', 'base': 'Фон_значення', 'options': 'Параметри', 'binary': 'бінарний', 'args': 'аргумент_масив', 'command': 'команда'}
    for 이전, чинний_елемент in зіставлення_значення.items():
        if hasattr(реалізація, чинний_елемент): globals()[이전] = getattr(реалізація, чинний_елемент)
