#!/usr/bin/env python3
"""기존 шлях 호환 запис_бал. фактично_дані реалізація: ../інструменти/파이썬빌드.py"""
import importlib as 가져오기
import sys as операційна_система_ОС_значення
from pathlib import Path as шлях
операційна_система_ОС_значення.path.insert(0, str(шлях(__file__).resolve().parents[1] / 'інструменти'))
if __name__ == '__main__':
    import runpy as програма_запускач
    програма_запускач.run_module('파이썬빌드', run_name='__main__', alter_sys=True)
else:
    реалізація = 가져오기.import_module('파이썬빌드')
    зіставлення_значення = {'ld': '연결편집기', 'archive': 'Архів', 'SHA256': 'перевірка_геш_код', 'build_python': '파이썬만들기', 'root': 'корінь_адреса', 'source': '원본자료', 'name': 'Назва', 'path': 'шлях', 'VERSION': 'випуск_значення', 'cc': '시언어번역기', 'tar': '타르꾸러미', 'newlib': '뉴리브포함경로', 'member': 'елемент'}
    for 이전, чинний_елемент in зіставлення_значення.items():
        if hasattr(реалізація, чинний_елемент): globals()[이전] = getattr(реалізація, чинний_елемент)
