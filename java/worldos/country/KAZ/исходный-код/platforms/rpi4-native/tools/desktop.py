#!/usr/bin/env python3
"""기존 путь 호환 точка_входа. фактический_данные реализация: ../инструменты/компьютер_Вид.py"""
import importlib as ВЗЯТЬ_ЗНАЧЕН
import sys as операционная_система_ЗНАЧЕН
from pathlib import Path as путь
операционная_система_ЗНАЧЕН.path.insert(0, str(путь(__file__).resolve().parents[1] / 'инструменты'))
if __name__ == '__main__':
    import runpy as программа_Launcher
    программа_Launcher.run_module('компьютер_Вид', run_name='__main__', alter_sys=True)
else:
    реализация = ВЗЯТЬ_ЗНАЧЕН.import_module('компьютер_Вид')
    сопоставление_ЗНАЧЕН = {'count': 'ввод_СЧЁТ', 'special': '특수글쇠', 'error': 'ошибка', 'exact': 'СОВПАД_ЗНАЧЕН', 'network': 'сеть', 'closed': 'ИТ_службы_закрыто', 'length': 'длина_ЗНАЧЕН', 'opened': '열림', 'ftp_port': 'передача_файла_номер_порта', 'server': 'сервер_ЗНАЧЕН', 'resources': 'Ресурсы', 'data': 'данные', 'shift': 'клавиша_SHIFT', 'send': 'написать', 'run_desktop': 'выполнить_компьютер', 'protocol': 'сеть_ABI', 'forwards': '전달규칙들', 'host': 'узел', 'text': 'текст', 'korean': '한글여부', 'port': 'номер_порта', 'signum': '신호번호', 'version': 'номер_версии', 'parser': 'анализатор', 'bridge': 'мост', 'kind': 'область_ЗНАЧЕН', 'tail': '끝부분', 'size': 'Размер', 'previous_buttons': '이전단추', 'key': '누름값', 'y': 'Y_координата', 'prefix': 'сдвиг_часть', 'client': 'клиент', 'char': 'символьные_данные', 'work': '작업경로', 'Keyboard': 'клавиатура', 'x': 'координата_X', 'down': '누르는중', 'net': 'мост_ввод', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'аргумент_МАССИВ', 'Hangul': '한글조합', 'chunk': 'блок_ЗНАЧЕН_652d4b53', 'proc': 'Процесс', 'Desktop': 'Connect_компьютер', 'buttons': '단추들', 'thread': 'фоноваяЗадача', 'pressed': '눌림', 'previous': 'Назад', 'toggle': 'перейти_МОДА', 'command': 'команда', 'sock': 'сокет_ЗНАЧЕН', 'frame': 'выполнение_кадр', 'ctrl': 'управление_Ключ', 'path': 'путь', 'cp': 'кодировка_символов', 'terminate': 'завершить', 'security': 'Безопасность', 'vnc_port': '원격화면접속번호', 'body': 'основной_текст', 'index': 'Поиск_ИНДЕКС', 'exited': '종료됨', 'keysym': 'Ключ_символ', 'output': 'выход', 'keyboard': 'клавиатура_ввод', 'interrupted': '가로채기됨', 'listener': 'порт_получения', 'reader': 'Ридер', 'NetworkBridge': 'мост_3de4fe3a', 'gui': 'рисунок_экран', 'worker': 'обработка_дело'}
    for Назад_товар, текущий_товар in сопоставление_ЗНАЧЕН.items():
        if hasattr(реализация, текущий_товар): globals()[Назад_товар] = getattr(реализация, текущий_товар)
