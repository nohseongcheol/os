#!/usr/bin/env python3
"""기존 ПЪТ 호환 запис_пункт. действителен_данни 구현: ../Инструменти/부팅시험.py"""
import importlib as 가져오기
import sys as операционна_система_стойност
from pathlib import Path as ПЪТ
операционна_система_стойност.path.insert(0, str(ПЪТ(__file__).resolve().parents[1] / 'Инструменти'))
if __name__ == '__main__':
    import runpy as програма_програма_за_стартиране
    програма_програма_за_стартиране.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('부팅시험')
    съпоставяне_стойност = {'timeout': '시간제한', 'response': 'отговор_1262b476', 'msg': 'мрежа_имейл', 'exact': '정확한값', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'Изпълнение', 'cancel': 'Отказ_операция', 'cmd_byte': 'команда_байт', 'reply': 'отговор', 'points': '지점들', 'server': 'сървър_стойност', 'data': 'данни', 'prompt': 'подкана', 'enter': 'въвеждам', 'imported': '들여온파일', 'send': 'изпращам', 'main': 'Стартиране', 'ROOT': 'проект_корен', 'text': 'Текст', 'first_gui': '첫화면', 'pixel': 'пиксел', 'java_class': '자바클래스', 'upload': 'качвам_Файлове', 'pixels_file': 'пиксел_Файл', 'pixels_data': 'пиксел_данни', 'edit': 'редакция_стойност', 'receive_until': '표시까지받기', 'selector': 'свързан_елемент_за_избор', 'size': 'Размер', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': '둘째화면', 'y': '세로좌표', 'result': 'РЕЗУЛТАТ', 'samples': '예제들', 'client': 'клиент', 'line': 'ред', 'report': 'проверка_отчет', 'work': '작업경로', 'x': 'x_координата', 'python_checks': '파이썬검사', 'download': 'изтеглям', 'greeting': '인사', 'dims': '치수', 'chunk': '조각', 'deadline': 'краен_срок_час', 'proc': 'Процес', 'content': 'Съдържание_стойност', 'block': 'блок_с_данни', 'marker': 'маркер', 'command': 'Команда', 'expected': '예상결과', 'shell': 'обвивка', 'drawing': 'чертеж_път', 'f': 'Файл_запис', 'transcript': 'препис', 'offset': 'Изместване_стойност', 'path': 'ПЪТ', 'screenshot': 'екранна_снимка', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': '화면접속자', 'output': '출력결과', 'stream': 'поток_стойност', 'cmd': '명령인수', 'name': 'Име', 'qmp': '모의제어접속'}
    for 이전, в_срок_артикул in съпоставяне_стойност.items():
        if hasattr(구현, в_срок_артикул): globals()[이전] = getattr(구현, в_срок_артикул)
