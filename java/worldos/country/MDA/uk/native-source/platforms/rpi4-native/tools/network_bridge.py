#!/usr/bin/env python3
"""기존 шлях 호환 запис_бал. фактично_дані реалізація: ../інструменти/міст_3de4fe3a.py"""
import importlib as 가져오기
import sys as операційна_система_ОС_значення
from pathlib import Path as шлях
операційна_система_ОС_значення.path.insert(0, str(шлях(__file__).resolve().parents[1] / 'інструменти'))
if __name__ == '__main__':
    import runpy as програма_запускач
    програма_запускач.run_module('міст_3de4fe3a', run_name='__main__', alter_sys=True)
else:
    реалізація = 가져오기.import_module('міст_3de4fe3a')
    зіставлення_значення = {'response': 'відгук', 'parts': 'шлях_компонент', 's': 'рядок_дані', 'i': '순번', 'close': 'Закрити', 'forward': '전달규칙', 'slip_input': '직렬전문입력', 'self': '자신', 'item': 'запис_значення_962f286b', 'flags': 'конфігурація_служба_фонового_передавання_файлів', 'ftp_port': 'передавання_файлу_номер_порту', 'args': 'аргумент_масив', 'server': 'сервер_значення', 'data': 'дані', 'ethernet_input': '이더넷입력', 'trace_packet': 'слід_пакет', 'GATEWAY': 'шлюз_обладнання_адреса', 'rule': 'лінія_значення', 'protocol': '통신규약', 'forwards': '전달규칙들', 'occupied': '사용중주소', 'host': 'хост', 'ack': '확인번호', 'serial_port': '직렬접속번호', 'readers': '읽기대상들', 'guest': 'гість', 'destination': 'місце_дані_адреса', 'ethernet_port': 'порт_Ethernet', 'b': '둘째값', 'MAC': 'дійсна_адреса', 'arp': 'адреса_роздільна_здатність_пакет', 'writable': '쓸수있음', 'direction': '방향', 'seq': '순서번호', 'frame': '실행틀', 'loop': 'цикл_значення', 'port': 'номер_порту', 'offset': 'Зміщена_копія_значення', 'readable': '읽을수있음', 'c': 'код_символу', 'p': 'дані_посада', 'writers': '쓰기대상들', 'IP': 'адреса_в_Інтернеті_значення', 'e': '보조항목', 'n': '개수', 'packet': 'пакет_дані', 'arguments': '전달인수', 'source': '원본자료', 'NetworkBridge': 'міст_3de4fe3a', 'window': 'Вікно', 'capture': 'записувати'}
    for 이전, чинний_елемент in зіставлення_значення.items():
        if hasattr(реалізація, чинний_елемент): globals()[이전] = getattr(реалізація, чинний_елемент)
