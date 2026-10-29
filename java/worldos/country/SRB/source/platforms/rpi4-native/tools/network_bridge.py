#!/usr/bin/env python3
"""기존 ПУТАЊА 호환 унос_поен. стваран_подаци 구현: ../Алатке/Мрежа_мост.py"""
import importlib as 가져오기
import sys as оперативни_систем_вриједност
from pathlib import Path as ПУТАЊА
оперативни_систем_вриједност.path.insert(0, str(ПУТАЊА(__file__).resolve().parents[1] / 'Алатке'))
if __name__ == '__main__':
    import runpy as програм_покретач
    програм_покретач.run_module('Мрежа_мост', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('Мрежа_мост')
    대응 = {'response': 'одговор_1262b476', 'parts': 'пут_компонента', 's': 'ниска_подаци', 'i': '순번', 'close': 'Затворен', 'forward': '전달규칙', 'slip_input': '직렬전문입력', 'self': '자신', 'item': 'унос_вриједност', 'flags': 'конфигурација_Услуга_интелигентног_преноса_у_позадини', 'ftp_port': 'фајл_пренос_број_порта', 'args': 'аргумент_низ', 'server': 'сервер_вриједност', 'data': 'подаци', 'ethernet_input': '이더넷입력', 'trace_packet': 'траг_пакет', 'GATEWAY': '관문기계주소', 'rule': 'филтер_вриједност', 'protocol': '통신규약', 'forwards': '전달규칙들', 'occupied': '사용중주소', 'host': 'хост', 'ack': '확인번호', 'serial_port': '직렬접속번호', 'readers': '읽기대상들', 'guest': 'гост', 'destination': 'одредиште_подаци_адреса', 'ethernet_port': 'Ethernet_порт', 'b': '둘째값', 'MAC': 'рачунар_адреса', 'arp': 'адреса_резолуција_пакет', 'writable': '쓸수있음', 'direction': '방향', 'seq': '순서번호', 'frame': '실행틀', 'loop': 'круг_вриједност', 'port': 'број_порта', 'offset': 'Помак_вриједност', 'readable': '읽을수있음', 'c': 'кôд_знака', 'p': 'подаци_позиција', 'writers': '쓰기대상들', 'IP': 'интернетска_адреса_вриједност', 'e': '보조항목', 'n': '개수', 'packet': 'пакет_подаци', 'arguments': '전달인수', 'source': '원본자료', 'NetworkBridge': 'Мрежа_мост', 'window': 'Прозор', 'capture': 'снимити'}
    for 이전, актуелно_ставка in 대응.items():
        if hasattr(구현, актуелно_ставка): globals()[이전] = getattr(구현, актуелно_ставка)
