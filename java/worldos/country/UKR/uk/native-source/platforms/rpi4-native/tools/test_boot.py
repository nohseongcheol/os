#!/usr/bin/env python3
"""기존 шлях 호환 запис_бал. фактично_дані реалізація: ../інструменти/부팅시험.py"""
import importlib as 가져오기
import sys as операційна_система_ОС_значення
from pathlib import Path as шлях
операційна_система_ОС_значення.path.insert(0, str(шлях(__file__).resolve().parents[1] / 'інструменти'))
if __name__ == '__main__':
    import runpy as програма_запускач
    програма_запускач.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    реалізація = 가져오기.import_module('부팅시험')
    зіставлення_значення = {'timeout': '시간제한', 'response': 'відгук', 'msg': 'мережа_повідомлення', 'exact': '정확한값', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'Виконати', 'cancel': 'Скасувати_операція', 'cmd_byte': 'команда_байт', 'reply': 'відповідь', 'points': '지점들', 'server': 'сервер_значення', 'data': 'дані', 'prompt': 'просити', 'enter': 'вводити', 'imported': '들여온파일', 'send': 'надсилати', 'main': 'запустити', 'ROOT': 'Дії_корінь', 'text': 'текст', 'first_gui': '첫화면', 'pixel': 'елемент_зображення', 'java_class': '자바클래스', 'upload': 'передавати_Файли', 'pixels_file': 'елемент_зображення_Файл', 'pixels_data': 'елемент_зображення_дані', 'edit': 'правка_значення', 'receive_until': '표시까지받기', 'selector': 'селектор', 'size': 'Розмір', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': '둘째화면', 'y': '세로좌표', 'result': 'результат', 'samples': '예제들', 'client': 'клієнт', 'line': 'рядок_введення', 'report': 'перевірка_звіт', 'work': '작업경로', 'x': 'координата_X', 'python_checks': '파이썬검사', 'download': 'завантажити', 'greeting': '인사', 'dims': '치수', 'chunk': '조각', 'deadline': 'крайнiй_термін_час', 'proc': 'Процеси', 'content': 'Вміст_значення', 'block': 'блок_даних', 'marker': 'маркер', 'command': 'команда', 'expected': '예상결과', 'shell': 'оболонка', 'drawing': 'малювання_шлях', 'f': 'Файл_запис', 'transcript': 'транскрипт', 'offset': 'Зміщена_копія_значення', 'path': 'шлях', 'screenshot': 'знімок_екрана', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': '화면접속자', 'output': '출력결과', 'stream': 'потік_значення', 'cmd': '명령인수', 'name': 'Назва', 'qmp': '모의제어접속'}
    for 이전, чинний_елемент in зіставлення_значення.items():
        if hasattr(реалізація, чинний_елемент): globals()[이전] = getattr(реалізація, чинний_елемент)
