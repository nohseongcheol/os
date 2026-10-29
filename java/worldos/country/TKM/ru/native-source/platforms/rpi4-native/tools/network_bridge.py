#!/usr/bin/env python3
"""기존 путь 호환 точка_входа. фактический_данные реализация: ../инструменты/мост_3de4fe3a.py"""
import importlib as ВЗЯТЬ_ЗНАЧЕН
import sys as операционная_система_ЗНАЧЕН
from pathlib import Path as путь
операционная_система_ЗНАЧЕН.path.insert(0, str(путь(__file__).resolve().parents[1] / 'инструменты'))
if __name__ == '__main__':
    import runpy as программа_Launcher
    программа_Launcher.run_module('мост_3de4fe3a', run_name='__main__', alter_sys=True)
else:
    реализация = ВЗЯТЬ_ЗНАЧЕН.import_module('мост_3de4fe3a')
    сопоставление_ЗНАЧЕН = {'response': 'ответ_1262b476', 'parts': 'путь_компонент', 's': 'строка_данные', 'i': '순번', 'close': 'Закрыть', 'forward': '전달규칙', 'slip_input': 'SLIP_входные_данные', 'self': '자신', 'item': 'ввод_ЗНАЧЕН', 'flags': 'настройки_BITS', 'ftp_port': 'передача_файла_номер_порта', 'args': 'аргумент_МАССИВ', 'server': 'сервер_ЗНАЧЕН', 'data': 'данные', 'ethernet_input': 'Ethernet_входные_данные', 'trace_packet': 'след_пакет', 'GATEWAY': 'шлюз_аппаратный_АДРЕС', 'rule': 'фильтр_ЗНАЧЕН', 'protocol': 'сеть_ABI', 'forwards': '전달규칙들', 'occupied': '사용중주소', 'host': 'узел', 'ack': '확인번호', 'serial_port': '직렬접속번호', 'readers': '읽기대상들', 'guest': 'гость', 'destination': 'цель_данные_АДРЕС', 'ethernet_port': 'порт_Ethernet', 'b': 'СЕКУНДЫ_ЗНАЧЕН', 'MAC': 'абсолютный_адрес', 'arp': 'АДРЕС_разрешение_пакет', 'writable': 'записываемый', 'direction': 'направление', 'seq': '순서번호', 'frame': 'выполнение_кадр', 'loop': 'цикл_ЗНАЧЕН', 'port': 'номер_порта', 'offset': 'СМЕЩ_ЗНАЧЕН', 'readable': '읽을수있음', 'c': 'код_знака', 'p': 'данные_позиция', 'writers': '쓰기대상들', 'IP': 'адрес_в_Интернете_ЗНАЧЕН', 'e': '보조항목', 'n': 'товар_СЧЁТ', 'packet': 'пакет_данные', 'arguments': '전달인수', 'source': '원본자료', 'NetworkBridge': 'мост_3de4fe3a', 'window': 'Окно', 'capture': 'Сбор'}
    for Назад_товар, текущий_товар in сопоставление_ЗНАЧЕН.items():
        if hasattr(реализация, текущий_товар): globals()[Назад_товар] = getattr(реализация, текущий_товар)
