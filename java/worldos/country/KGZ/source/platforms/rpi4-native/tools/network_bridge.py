#!/usr/bin/env python3
"""기존 ЖОЛ 호환 киргизме_жазуу_упай. актуалдуу_берилмелер 구현: ../Куралдар/통신다리.py"""
import importlib as 가져오기
import sys as оперативдик_система_маани
from pathlib import Path as ЖОЛ
оперативдик_система_маани.path.insert(0, str(ЖОЛ(__file__).resolve().parents[1] / 'Куралдар'))
if __name__ == '__main__':
    import runpy as програм_жаратма_тарткычы
    програм_жаратма_тарткычы.run_module('통신다리', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('통신다리')
    대응 = {'response': '응답자료', 'parts': 'жол_курамдык_бөлүк', 's': 'сап_берилмелер', 'i': '순번', 'close': 'Жабуу', 'forward': '전달규칙', 'slip_input': '직렬전문입력', 'self': '자신', 'item': 'киргизме_жазуу_маани', 'flags': '설정비트', 'ftp_port': '파일전송접속번호', 'args': 'аргумент_МАССИВ', 'server': 'сервер_маани', 'data': 'берилмелер', 'ethernet_input': '이더넷입력', 'trace_packet': '전문추적', 'GATEWAY': '관문기계주소', 'rule': 'чыпка_маани', 'protocol': '통신규약', 'forwards': '전달규칙들', 'occupied': '사용중주소', 'host': 'кабылдоо', 'ack': '확인번호', 'serial_port': '직렬접속번호', 'readers': '읽기대상들', 'guest': '커널실행', 'destination': 'көздөө_жайы_берилмелер_дарек', 'ethernet_port': '이더넷접속번호', 'b': '둘째값', 'MAC': 'машина_дарек', 'arp': 'дарек_чечим_пакет', 'writable': '쓸수있음', 'direction': '방향', 'seq': '순서번호', 'frame': '실행틀', 'loop': 'Айлампа_маани', 'port': '접속번호', 'offset': 'Жылбышуу_маани', 'readable': '읽을수있음', 'c': 'символ_коду', 'p': '자료위치', 'writers': '쓰기대상들', 'IP': 'Интернет_дарек_маани', 'e': '보조항목', 'n': '개수', 'packet': 'пакет_берилмелер', 'arguments': '전달인수', 'source': '원본자료', 'NetworkBridge': '통신다리', 'window': 'терезе', 'capture': 'тартуу_жаздыруу'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
