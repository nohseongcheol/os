#!/usr/bin/env python3
"""기존 Жол_2 호환 енгізу_ұпай. нақты_деректер 구현: ../Құралдар/셸시험.py"""
import importlib as 가져오기
import sys as операциялық_жүйе_мән
from pathlib import Path as Жол_2
операциялық_жүйе_мән.path.insert(0, str(Жол_2(__file__).resolve().parents[1] / 'Құралдар'))
if __name__ == '__main__':
    import runpy as бағдарлама_іске_қосу_құралы
    бағдарлама_іске_қосу_құралы.run_module('셸시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('셸시험')
    대응 = {'timeout': '시간제한', 'x': 'x_координатасы', 'msg': 'желі_хабар', 'i': '순번', 'reply': 'жауап', 'call': '호출', 'args': 'аргумент_массив', 'chunk': '조각', 'data': 'деректер', 'proc': 'Үрдіс', 'long_text': '긴글', 'restored': '복원자료', 'send': 'жіберу', 'file': 'Файл', 'main': 'Орындау_2', 'found': 'Іздеу_өлшем', 'ROOT': 'жоба_түбір', 'text': 'Мәтін', 'marker': '확인표시', 'command': 'Команда', 'expected': '예상결과', 'pixel': 'нүкте', 'shell': 'қоршам', 'poll': '준비살피미', 'transcript': '대화기록', 'end': 'тоқтату_жылжыту', 'image': 'сурет', 'key': '누름값', 'y': 'Y_түймешігі_координата', 'output': '출력결과', 'result': 'НӘТИЖЕ', 'client': 'клиент', 'line': 'Жол', 'stream': 'ағым_мән', 'name': 'Аты', 'value': 'мән', 'receive': '수신하기', 'report': 'тексерім_есеп', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, ток_элемент in 대응.items():
        if hasattr(구현, ток_элемент): globals()[이전] = getattr(구현, ток_элемент)
