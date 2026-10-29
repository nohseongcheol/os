#!/usr/bin/env python3
"""기존 шлях 호환 запис_бал. фактично_дані реалізація: ../інструменти/настільний_Вигляд.py"""
import importlib as 가져오기
import sys as операційна_система_ОС_значення
from pathlib import Path as шлях
операційна_система_ОС_значення.path.insert(0, str(шлях(__file__).resolve().parents[1] / 'інструменти'))
if __name__ == '__main__':
    import runpy as програма_запускач
    програма_запускач.run_module('настільний_Вигляд', run_name='__main__', alter_sys=True)
else:
    реалізація = 가져오기.import_module('настільний_Вигляд')
    зіставлення_значення = {'count': '항목수', 'special': '특수글쇠', 'error': 'ПОМИЛКА', 'exact': '정확한값', 'network': 'мережа', 'closed': '닫힘', 'length': '길이', 'opened': '열림', 'ftp_port': 'передавання_файлу_номер_порту', 'server': 'сервер_значення', 'resources': 'Ресурси', 'data': 'дані', 'shift': '윗글쇠', 'send': 'надсилати', 'run_desktop': 'запускати_настільний', 'protocol': '통신규약', 'forwards': '전달규칙들', 'host': 'хост', 'text': 'текст', 'korean': '한글여부', 'port': 'номер_порту', 'signum': '신호번호', 'version': 'номер_версії', 'parser': 'аналізатор', 'bridge': 'міст', 'kind': 'область_значення', 'tail': '끝부분', 'size': 'Розмір', 'previous_buttons': '이전단추', 'key': '누름값', 'y': '세로좌표', 'prefix': '앞부분', 'client': 'клієнт', 'char': 'символьні_дані', 'work': '작업경로', 'Keyboard': 'клавіатура', 'x': 'координата_X', 'down': '누르는중', 'net': 'міст_запис', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'аргумент_масив', 'Hangul': '한글조합', 'chunk': '조각', 'proc': 'Процеси', 'Desktop': 'зв_язок_настільний', 'buttons': '단추들', 'thread': 'фоноваЗадача', 'pressed': '눌림', 'previous': '이전항목', 'toggle': 'перехід_режим', 'command': 'команда', 'sock': 'сокет_значення', 'frame': '실행틀', 'ctrl': 'керування_Ключ', 'path': 'шлях', 'cp': 'кодування_символів', 'terminate': '종료시키기', 'security': 'захист', 'vnc_port': '원격화면접속번호', 'body': 'основний_текст', 'index': 'Інформування_індекс', 'exited': '종료됨', 'keysym': 'Ключ_символ', 'output': '출력결과', 'keyboard': 'клавіатура_запис', 'interrupted': '가로채기됨', 'listener': 'отримувати_порт', 'reader': 'читач', 'NetworkBridge': 'міст_3de4fe3a', 'gui': '그림화면', 'worker': 'обробка_справа'}
    for 이전, чинний_елемент in зіставлення_значення.items():
        if hasattr(реалізація, чинний_елемент): globals()[이전] = getattr(реалізація, чинний_елемент)
