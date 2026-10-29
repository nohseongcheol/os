#!/usr/bin/env python3
"""기존 ПАТЕКА 호환 внес_поен. реален_податоци 구현: ../Алатки/Мрежа_мост.py"""
import importlib as TAKE_VALUE
import sys as оперативен_систем_VALUE
from pathlib import Path as ПАТЕКА
оперативен_систем_VALUE.path.insert(0, str(ПАТЕКА(__file__).resolve().parents[1] / 'Алатки'))
if __name__ == '__main__':
    import runpy as програма_стартувач
    програма_стартувач.run_module('Мрежа_мост', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('Мрежа_мост')
    대응 = {'response': '응답자료', 'parts': 'патека_компонента', 's': 'низа_податоци', 'i': '순번', 'close': 'Затвори', 'forward': '전달규칙', 'slip_input': '직렬전문입력', 'self': '자신', 'item': 'внес_VALUE', 'flags': 'конфигурација_Услуга_за_интелигентен_пренос_во_заднина', 'ftp_port': 'датотека_пренос_број_на_порта', 'args': 'аргумент_низа', 'server': 'сервер_VALUE', 'data': 'податоци', 'ethernet_input': '이더넷입력', 'trace_packet': 'трага_пакет', 'GATEWAY': '관문기계주소', 'rule': 'филтер_VALUE', 'protocol': '통신규약', 'forwards': '전달규칙들', 'occupied': '사용중주소', 'host': 'вдоми', 'ack': '확인번호', 'serial_port': '직렬접속번호', 'readers': '읽기대상들', 'guest': 'гостин', 'destination': 'одредиште_податоци_адреса', 'ethernet_port': 'Етернет_порта', 'b': 'SECOND_VALUE', 'MAC': 'машина_адреса', 'arp': 'адреса_резолуција_пакет', 'writable': '쓸수있음', 'direction': '방향', 'seq': '순서번호', 'frame': '실행틀', 'loop': 'Циклус_VALUE', 'port': 'број_на_порта', 'offset': 'OFFSET_VALUE', 'readable': '읽을수있음', 'c': 'кодна_точка', 'p': 'податоци_позиционирање', 'writers': '쓰기대상들', 'IP': 'Интернет_адреса_VALUE', 'e': '보조항목', 'n': 'ставка_COUNT', 'packet': 'пакет_податоци', 'arguments': '전달인수', 'source': '원본자료', 'NetworkBridge': 'Мрежа_мост', 'window': 'прозорец', 'capture': 'зафати'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
