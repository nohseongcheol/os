#!/usr/bin/env python3
"""기존 Жол_2 호환 енгізу_ұпай. нақты_деректер 구현: ../Құралдар/желі_көпір.py"""
import importlib as 가져오기
import sys as операциялық_жүйе_мән
from pathlib import Path as Жол_2
операциялық_жүйе_мән.path.insert(0, str(Жол_2(__file__).resolve().parents[1] / 'Құралдар'))
if __name__ == '__main__':
    import runpy as бағдарлама_іске_қосу_құралы
    бағдарлама_іске_қосу_құралы.run_module('желі_көпір', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('желі_көпір')
    대응 = {'response': 'жауап_1262b476', 'parts': 'жол_құрамдас', 's': 'жол_деректер', 'i': '순번', 'close': 'Жабу', 'forward': '전달규칙', 'slip_input': '직렬전문입력', 'self': '자신', 'item': 'енгізу_мән', 'flags': 'конфигурация_фондық_интеллектуалдық_тасымалдау_қызметі', 'ftp_port': 'файл_тасымалдау_порт_нөмірі', 'args': 'аргумент_массив', 'server': 'сервер_мән', 'data': 'деректер', 'ethernet_input': '이더넷입력', 'trace_packet': 'із_пакет', 'GATEWAY': '관문기계주소', 'rule': 'ереже_мән', 'protocol': '통신규약', 'forwards': '전달규칙들', 'occupied': '사용중주소', 'host': 'орналастыру', 'ack': '확인번호', 'serial_port': '직렬접속번호', 'readers': '읽기대상들', 'guest': 'қонақ', 'destination': 'тағайындау_деректер_мекенжай', 'ethernet_port': 'Ethernet_порты', 'b': '둘째값', 'MAC': 'нақпа_нақ_мекенжай', 'arp': 'мекенжай_ажыратымдылық_пакет', 'writable': '쓸수있음', 'direction': '방향', 'seq': '순서번호', 'frame': '실행틀', 'loop': 'Айналым_мән', 'port': 'порт_нөмірі', 'offset': 'жылжыту_мән_450fc799', 'readable': '읽을수있음', 'c': 'таңба_коды', 'p': 'деректер_лауазым', 'writers': '쓰기대상들', 'IP': 'Интернет_мекенжайы_мән', 'e': '보조항목', 'n': '개수', 'packet': 'пакет_деректер', 'arguments': '전달인수', 'source': '원본자료', 'NetworkBridge': 'желі_көпір', 'window': 'Терезе', 'capture': 'түсіру'}
    for 이전, ток_элемент in 대응.items():
        if hasattr(구현, ток_элемент): globals()[이전] = getattr(구현, ток_элемент)
