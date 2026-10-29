#!/usr/bin/env python3
"""기존 ЗАМ 호환 оролт_цэг. бодит_өгөгдөл 구현: ../Хэрэгслүүд/통신다리.py"""
import importlib as 가져오기
import sys as үйлдлийн_систем_утга
from pathlib import Path as ЗАМ
үйлдлийн_систем_утга.path.insert(0, str(ЗАМ(__file__).resolve().parents[1] / 'Хэрэгслүүд'))
if __name__ == '__main__':
    import runpy as програм_гишүүн
    програм_гишүүн.run_module('통신다리', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('통신다리')
    대응 = {'response': '응답자료', 'parts': 'зам_бүрэлдэхүүн', 's': 'мөр_өгөгдөл', 'i': '순번', 'close': 'Хаах', 'forward': '전달규칙', 'slip_input': '직렬전문입력', 'self': '자신', 'item': 'оролт_утга', 'flags': '설정비트', 'ftp_port': '파일전송접속번호', 'args': 'аргумент_олонлог', 'server': 'сервер_утга', 'data': 'өгөгдөл', 'ethernet_input': '이더넷입력', 'trace_packet': '전문추적', 'GATEWAY': '관문기계주소', 'rule': 'дүрэм_утга', 'protocol': '통신규약', 'forwards': '전달규칙들', 'occupied': '사용중주소', 'host': 'хост', 'ack': '확인번호', 'serial_port': '직렬접속번호', 'readers': '읽기대상들', 'guest': '커널실행', 'destination': 'товлосон_газар_өгөгдөл_хаяг', 'ethernet_port': 'этернэт_порт', 'b': '둘째값', 'MAC': 'компьютер_хаяг', 'arp': 'хаяг_нягтрал_пакет', 'writable': '쓸수있음', 'direction': '방향', 'seq': '순서번호', 'frame': '실행틀', 'loop': 'цикль_утга', 'port': '접속번호', 'offset': 'Оффсет_утга', 'readable': '읽을수있음', 'c': 'тэмдэгтийн_код', 'p': '자료위치', 'writers': '쓰기대상들', 'IP': 'Интернет_хаяг_утга', 'e': '보조항목', 'n': '개수', 'packet': 'пакет_өгөгдөл', 'arguments': '전달인수', 'source': '원본자료', 'NetworkBridge': '통신다리', 'window': 'цонх', 'capture': 'авах'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
