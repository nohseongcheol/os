#!/usr/bin/env python3
"""기존 шлях 호환 запис_бал. фактично_дані реалізація: ../інструменти/자바라이브러리빌드.py"""
import importlib as 가져오기
import sys as операційна_система_ОС_значення
from pathlib import Path as шлях
операційна_система_ОС_значення.path.insert(0, str(шлях(__file__).resolve().parents[1] / 'інструменти'))
if __name__ == '__main__':
    import runpy as програма_запускач
    програма_запускач.run_module('자바라이브러리빌드', run_name='__main__', alter_sys=True)
else:
    реалізація = 가져오기.import_module('자바라이브러리빌드')
    зіставлення_значення = {'header': 'Заголовок_значення', 'sources': '원문목록', 'i': '순번', 'info': 'Відомості_про_систему', 'payload': 'вміст_пакета_дані', 'src': '원본주소', 'run': 'Виконати_команда', 'build_java_library': '자바라이브러리만들기', 'relative': 'відносний_шлях', 'classes': 'Клас_шлях', 'dist': '배포경로', 'archive': 'Архів', 'output': '출력결과', 'root': 'корінь_адреса', 'name': 'Назва', 'jar': '자바꾸러미', 'b': '둘째값', 'entries': '항목들'}
    for 이전, чинний_елемент in зіставлення_значення.items():
        if hasattr(реалізація, чинний_елемент): globals()[이전] = getattr(реалізація, чинний_елемент)
