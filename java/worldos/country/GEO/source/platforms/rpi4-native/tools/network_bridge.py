#!/usr/bin/env python3
"""기존 გეზი 호환 შენატანი_პტ. რეალური_მონაცემები 구현: ../ხელსაწყოები/ქსელი_ხიდი.py"""
import importlib as 가져오기
import sys as ოპერაციული_სისტემა_მნიშვნელობა
from pathlib import Path as გეზი
ოპერაციული_სისტემა_მნიშვნელობა.path.insert(0, str(გეზი(__file__).resolve().parents[1] / 'ხელსაწყოები'))
if __name__ == '__main__':
    import runpy as აპი_გამშვები
    აპი_გამშვები.run_module('ქსელი_ხიდი', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ქსელი_ხიდი')
    대응 = {'response': 'პასუხი_1262b476', 'parts': 'მდებარეობა_კომპონენტი', 's': 'სტრიქონი_მონაცემები', 'i': '순번', 'close': 'დახურვა', 'forward': '전달규칙', 'slip_input': '직렬전문입력', 'self': '자신', 'item': 'შენატანი_მნიშვნელობა', 'flags': '설정비트', 'ftp_port': '파일전송접속번호', 'args': 'არგუმენტი_მასივი', 'server': 'სერვერი_მნიშვნელობა', 'data': 'მონაცემები', 'ethernet_input': '이더넷입력', 'trace_packet': '전문추적', 'GATEWAY': '관문기계주소', 'rule': 'წესი_მნიშვნელობა', 'protocol': '통신규약', 'forwards': '전달규칙들', 'occupied': '사용중주소', 'host': 'მასპინძელი', 'ack': '확인번호', 'serial_port': '직렬접속번호', 'readers': '읽기대상들', 'guest': 'სტუმარი', 'destination': 'მიმართულება_მონაცემები_მისამართი', 'ethernet_port': 'ეთერნეტის_პორტი', 'b': '둘째값', 'MAC': 'კომპიუტერი_მისამართი', 'arp': '주소찾기전문', 'writable': '쓸수있음', 'direction': '방향', 'seq': '순서번호', 'frame': '실행틀', 'loop': 'ციკლი_მნიშვნელობა', 'port': '접속번호', 'offset': 'ოფსეტი_მნიშვნელობა', 'readable': '읽을수있음', 'c': 'სიმბოლოს_კოდი', 'p': 'მონაცემები_პოზიცია', 'writers': '쓰기대상들', 'IP': 'ინტერნეტის_მისამართი_მნიშვნელობა', 'e': '보조항목', 'n': '개수', 'packet': '꾸러미자료', 'arguments': '전달인수', 'source': '원본자료', 'NetworkBridge': 'ქსელი_ხიდი', 'window': 'ფანჯარა', 'capture': 'გადაღება'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
