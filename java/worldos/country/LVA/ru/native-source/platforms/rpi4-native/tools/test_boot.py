#!/usr/bin/env python3
"""기존 путь 호환 точка_входа. фактический_данные реализация: ../инструменты/부팅시험.py"""
import importlib as ВЗЯТЬ_ЗНАЧЕН
import sys as операционная_система_ЗНАЧЕН
from pathlib import Path as путь
операционная_система_ЗНАЧЕН.path.insert(0, str(путь(__file__).resolve().parents[1] / 'инструменты'))
if __name__ == '__main__':
    import runpy as программа_Launcher
    программа_Launcher.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    реализация = ВЗЯТЬ_ЗНАЧЕН.import_module('부팅시험')
    сопоставление_ЗНАЧЕН = {'timeout': 'выполнение_ТАЙМАУТ', 'response': 'ответ_1262b476', 'msg': 'сеть_письмо', 'exact': 'СОВПАД_ЗНАЧЕН', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'Выполнить', 'cancel': 'Close_операция', 'cmd_byte': '명령바이트', 'reply': 'ответ', 'points': '지점들', 'server': 'сервер_ЗНАЧЕН', 'data': 'данные', 'prompt': 'запрос_1dd14da4', 'enter': 'ввести', 'imported': '들여온파일', 'send': 'написать', 'main': 'запустить', 'ROOT': 'задача_корень', 'text': 'текст', 'first_gui': '첫화면', 'pixel': 'пиксель', 'java_class': '자바클래스', 'upload': 'Upload_Файлы', 'pixels_file': 'пиксель_файл', 'pixels_data': 'пиксель_данные', 'edit': 'правка_ЗНАЧЕН', 'receive_until': '표시까지받기', 'selector': 'селектор', 'size': 'Размер', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': 'СЕКУНДЫ_графический_пользовательский_интерфейс', 'y': 'Y_координата', 'result': 'результат', 'samples': '예제들', 'client': 'клиент', 'line': 'строка_ввода', 'report': 'проверка_Отчет', 'work': '작업경로', 'x': 'координата_X', 'python_checks': '파이썬검사', 'download': 'скачать', 'greeting': 'приветствие_ae353e94', 'dims': '치수', 'chunk': 'блок_ЗНАЧЕН_652d4b53', 'deadline': 'крайний_срок_ВРЕМЯ', 'proc': 'Процесс', 'content': 'контент_ЗНАЧЕН', 'block': 'блок_данных', 'marker': 'метка', 'command': 'команда', 'expected': '예상결과', 'shell': 'оболочка', 'drawing': 'рисунок_путь', 'f': 'файл_ввод', 'transcript': 'расшифровка', 'offset': 'СМЕЩ_ЗНАЧЕН', 'path': 'путь', 'screenshot': 'снимок_экрана', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': 'экран_клиент', 'output': 'выход', 'stream': 'поток_ЗНАЧЕН', 'cmd': '명령인수', 'name': 'Название', 'qmp': '모의제어접속'}
    for Назад_товар, текущий_товар in сопоставление_ЗНАЧЕН.items():
        if hasattr(реализация, текущий_товар): globals()[Назад_товар] = getattr(реализация, текущий_товар)
