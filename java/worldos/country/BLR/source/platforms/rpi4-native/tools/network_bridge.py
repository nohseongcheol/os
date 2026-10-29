#!/usr/bin/env python3
"""기존 ШЛЯХ 호환 увядзенне_бал. фактычны_дадзеныя 구현: ../Інструменты/Сетка_мост.py"""
import importlib as 가져오기
import sys as аперацыйная_сістэма_значэнне
from pathlib import Path as ШЛЯХ
аперацыйная_сістэма_значэнне.path.insert(0, str(ШЛЯХ(__file__).resolve().parents[1] / 'Інструменты'))
if __name__ == '__main__':
    import runpy as праграма_выклік_праграм
    праграма_выклік_праграм.run_module('Сетка_мост', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('Сетка_мост')
    대응 = {'response': '응답자료', 'parts': 'шлях_кампанент', 's': 'радок_дадзеныя', 'i': '순번', 'close': 'Закрыць', 'forward': '전달규칙', 'slip_input': '직렬전문입력', 'self': '자신', 'item': 'увядзенне_значэнне', 'flags': 'канфігурацыя_Служба_інтэлектуальнай_фонавай_перадачы_файлаў', 'ftp_port': 'файл_перанос_нумар_порта', 'args': 'аргумент_масіў', 'server': 'сервер_значэнне', 'data': 'дадзеныя', 'ethernet_input': '이더넷입력', 'trace_packet': 'след_пакет', 'GATEWAY': '관문기계주소', 'rule': 'фільтр_значэнне', 'protocol': '통신규약', 'forwards': '전달규칙들', 'occupied': '사용중주소', 'host': 'вузел', 'ack': '확인번호', 'serial_port': '직렬접속번호', 'readers': '읽기대상들', 'guest': 'госць', 'destination': 'прызначэнне_дадзеныя_адрас', 'ethernet_port': '이더넷접속번호', 'b': '둘째값', 'MAC': 'камп_ютар_адрас', 'arp': 'адрас_разрознасць_пакет', 'writable': '쓸수있음', 'direction': '방향', 'seq': '순서번호', 'frame': '실행틀', 'loop': 'Цыклічная_значэнне', 'port': 'нумар_порта', 'offset': 'Зрух_значэнне', 'readable': '읽을수있음', 'c': 'код_сімвала', 'p': '자료위치', 'writers': '쓰기대상들', 'IP': 'інтэрнэт_адрас_значэнне', 'e': '보조항목', 'n': '개수', 'packet': 'пакет_дадзеныя', 'arguments': '전달인수', 'source': '원본자료', 'NetworkBridge': 'Сетка_мост', 'window': 'акно', 'capture': 'зняць'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
