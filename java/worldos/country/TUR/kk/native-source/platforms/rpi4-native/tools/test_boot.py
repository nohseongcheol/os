#!/usr/bin/env python3
"""기존 Жол_2 호환 енгізу_ұпай. нақты_деректер 구현: ../Құралдар/부팅시험.py"""
import importlib as 가져오기
import sys as операциялық_жүйе_мән
from pathlib import Path as Жол_2
операциялық_жүйе_мән.path.insert(0, str(Жол_2(__file__).resolve().parents[1] / 'Құралдар'))
if __name__ == '__main__':
    import runpy as бағдарлама_іске_қосу_құралы
    бағдарлама_іске_қосу_құралы.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('부팅시험')
    대응 = {'timeout': '시간제한', 'response': 'жауап_1262b476', 'msg': 'желі_хабар', 'exact': '정확한값', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'Орындау', 'cancel': 'бас_тарту_ота', 'cmd_byte': 'пәрмен_байт', 'reply': 'жауап', 'points': '지점들', 'server': 'сервер_мән', 'data': 'деректер', 'prompt': 'сұрау', 'enter': 'енгізу', 'imported': '들여온파일', 'send': 'жіберу', 'main': 'Орындау_2', 'ROOT': 'жоба_түбір', 'text': 'Мәтін', 'first_gui': '첫화면', 'pixel': 'нүкте', 'java_class': '자바클래스', 'upload': 'Жүктеп_салу_Файлдар', 'pixels_file': 'нүкте_файл', 'pixels_data': 'нүкте_деректер', 'edit': 'өңдеу_мән', 'receive_until': '표시까지받기', 'selector': 'селектор', 'size': 'Өлшемі', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': '둘째화면', 'y': 'Y_түймешігі_координата', 'result': 'НӘТИЖЕ', 'samples': '예제들', 'client': 'клиент', 'line': 'Жол', 'report': 'тексерім_есеп', 'work': '작업경로', 'x': 'x_координатасы', 'python_checks': '파이썬검사', 'download': 'жүктеме', 'greeting': '인사', 'dims': '치수', 'chunk': '조각', 'deadline': 'ең_соңғы_мерзім_уақыт', 'proc': 'Үрдіс', 'content': 'мазмұн_мән', 'block': 'деректер_блогы', 'marker': '확인표시', 'command': 'Команда', 'expected': '예상결과', 'shell': 'қоршам', 'drawing': 'сызба_жол', 'f': 'файл_енгізу', 'transcript': '대화기록', 'offset': 'жылжыту_мән_450fc799', 'path': 'Жол_2', 'screenshot': 'скриншот', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': '화면접속자', 'output': '출력결과', 'stream': 'ағым_мән', 'cmd': '명령인수', 'name': 'Аты', 'qmp': '모의제어접속'}
    for 이전, ток_элемент in 대응.items():
        if hasattr(구현, ток_элемент): globals()[이전] = getattr(구현, ток_элемент)
