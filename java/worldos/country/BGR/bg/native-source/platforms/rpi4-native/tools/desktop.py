#!/usr/bin/env python3
"""기존 ПЪТ 호환 запис_пункт. действителен_данни 구현: ../Инструменти/десктоп_Изглед.py"""
import importlib as 가져오기
import sys as операционна_система_стойност
from pathlib import Path as ПЪТ
операционна_система_стойност.path.insert(0, str(ПЪТ(__file__).resolve().parents[1] / 'Инструменти'))
if __name__ == '__main__':
    import runpy as програма_програма_за_стартиране
    програма_програма_за_стартиране.run_module('десктоп_Изглед', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('десктоп_Изглед')
    съпоставяне_стойност = {'count': '항목수', 'special': '특수글쇠', 'error': 'ГРЕШКА', 'exact': '정확한값', 'network': 'мрежа', 'closed': '닫힘', 'length': '길이', 'opened': '열림', 'ftp_port': 'прехвърляне_на_файл_номер_на_порт', 'server': 'сървър_стойност', 'resources': 'Ресурси', 'data': 'данни', 'shift': '윗글쇠', 'send': 'изпращам', 'run_desktop': 'изпълнение_десктоп', 'protocol': '통신규약', 'forwards': '전달규칙들', 'host': 'хост', 'text': 'Текст', 'korean': '한글여부', 'port': 'номер_на_порт', 'signum': '신호번호', 'version': 'номер_на_версия', 'parser': 'анализатор', 'bridge': 'мост', 'kind': 'област_стойност', 'tail': '끝부분', 'size': 'Размер', 'previous_buttons': '이전단추', 'key': '누름값', 'y': '세로좌표', 'prefix': '앞부분', 'client': 'клиент', 'char': 'знакови_данни', 'work': '작업경로', 'Keyboard': 'клавиатура', 'x': 'x_координата', 'down': '누르는중', 'net': 'мост_запис', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'аргумент_масив', 'Hangul': '한글조합', 'chunk': '조각', 'proc': 'Процес', 'Desktop': 'връзка_десктоп', 'buttons': '단추들', 'thread': '작업가닥', 'pressed': '눌림', 'previous': '이전항목', 'toggle': 'комутатор_режим', 'command': 'Команда', 'sock': '소켓', 'frame': '실행틀', 'ctrl': 'контрол_Ключ', 'path': 'ПЪТ', 'cp': 'знаково_кодиране', 'terminate': '종료시키기', 'security': 'Защита', 'vnc_port': '원격화면접속번호', 'body': 'основен_текст', 'index': 'Търсене_индекс', 'exited': '종료됨', 'keysym': 'Ключ_символ', 'output': '출력결과', 'keyboard': 'клавиатура_запис', 'interrupted': '가로채기됨', 'listener': 'получавам_порт', 'reader': 'читател', 'NetworkBridge': 'мост_3de4fe3a', 'gui': '그림화면', 'worker': 'обработка_задача'}
    for 이전, в_срок_артикул in съпоставяне_стойност.items():
        if hasattr(구현, в_срок_артикул): globals()[이전] = getattr(구현, в_срок_артикул)
