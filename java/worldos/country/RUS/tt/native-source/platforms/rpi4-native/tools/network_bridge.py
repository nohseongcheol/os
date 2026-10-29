#!/usr/bin/env python3
"""기존 Yul 호환 кертү_балл. фактик_мәгълүмат 구현: ../Кораллар/Челтәр_күпер.py"""
import importlib as TAKE_VALUE
import sys as операцион_система_VALUE
from pathlib import Path as Yul
операцион_система_VALUE.path.insert(0, str(Yul(__file__).resolve().parents[1] / 'Кораллар'))
if __name__ == '__main__':
    import runpy as кушымта_хезмәткәр
    кушымта_хезмәткәр.run_module('Челтәр_күпер', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('Челтәр_күпер')
    대응 = {'response': '응답자료', 'parts': 'юл_компонент', 's': 'юл_мәгълүмат', 'i': '순번', 'close': 'Yap', 'forward': '전달규칙', 'slip_input': '직렬전문입력', 'self': '자신', 'item': 'кертү_VALUE', 'flags': '설정비트', 'ftp_port': '파일전송접속번호', 'args': 'аргумент_МАССИВ', 'server': 'сервер_VALUE', 'data': 'мәгълүмат', 'ethernet_input': '이더넷입력', 'trace_packet': '전문추적', 'GATEWAY': '관문기계주소', 'rule': 'сөзгеч_VALUE', 'protocol': '통신규약', 'forwards': '전달규칙들', 'occupied': '사용중주소', 'host': 'хост', 'ack': '확인번호', 'serial_port': '직렬접속번호', 'readers': '읽기대상들', 'guest': 'кунак', 'destination': 'күчерү_урыны_мәгълүмат_адрес', 'ethernet_port': 'Ethernet_порт', 'b': 'SECOND_VALUE', 'MAC': 'машина_адрес', 'arp': '주소찾기전문', 'writable': '쓸수있음', 'direction': '방향', 'seq': '순서번호', 'frame': '실행틀', 'loop': 'Цикл_VALUE', 'port': '접속번호', 'offset': 'OFFSET_VALUE', 'readable': '읽을수있음', 'c': 'символ_коды', 'p': 'мәгълүмат_урнаштыру', 'writers': '쓰기대상들', 'IP': 'Интернеттагы_адрес_VALUE', 'e': '보조항목', 'n': 'элемент_COUNT', 'packet': '꾸러미자료', 'arguments': '전달인수', 'source': '원본자료', 'NetworkBridge': 'Челтәр_күпер', 'window': 'тәрәз', 'capture': 'яздыру'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
