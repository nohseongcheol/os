#!/usr/bin/env python3
"""기존 шлях 호환 запис_бал. фактично_дані реалізація: ../інструменти/실행파일시험.py"""
import importlib as 가져오기
import sys as операційна_система_ОС_значення
from pathlib import Path as шлях
операційна_система_ОС_значення.path.insert(0, str(шлях(__file__).resolve().parents[1] / 'інструменти'))
if __name__ == '__main__':
    import runpy as програма_запускач
    програма_запускач.run_module('실행파일시험', run_name='__main__', alter_sys=True)
else:
    реалізація = 가져오기.import_module('실행파일시험')
    зіставлення_значення = {'out': 'КР_дані', 'expected': '예상결과', 'phoff': 'програма_Заголовок_Зміщена_копія', 'offset': 'Зміщена_копія_значення', 'invalid': 'недійсний_дані', 'path': 'шлях', 'executable': '실행가능파일', 'rejected': '거부결과', 'linux_example': '리눅스예제', 'original': '원본', 'result': 'результат', 'format_': 'формат_b87fd068', 'main': 'запустити', 'content': 'Вміст_значення', 'source': '원본자료', 'name': 'Назва', 'reference': 'Порівняння_напрямна', 'ROOT': 'Дії_корінь', 'value': 'значення', 'report': 'перевірка_звіт'}
    for 이전, чинний_елемент in зіставлення_значення.items():
        if hasattr(реалізація, чинний_елемент): globals()[이전] = getattr(реалізація, чинний_елемент)
