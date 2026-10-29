#!/usr/bin/env python3
"""기존 مسیر 호환 ورودی_نقطه. واقعی_داده_ها 구현: ../ابزارها/شبکه_پل.py"""
import importlib as 가져오기
import sys as سیستم_عامل_مقدار
from pathlib import Path as مسیر
سیستم_عامل_مقدار.path.insert(0, str(مسیر(__file__).resolve().parents[1] / 'ابزارها'))
if __name__ == '__main__':
    import runpy as برنامه_راه_انداز
    برنامه_راه_انداز.run_module('شبکه_پل', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('شبکه_پل')
    대응 = {'response': '응답자료', 'parts': 'مسیر_مؤلفه', 's': 'رشته_داده_ها', 'i': '순번', 'close': 'بستن', 'forward': '전달규칙', 'slip_input': '직렬전문입력', 'self': '자신', 'item': 'ورودی_مقدار', 'flags': '설정비트', 'ftp_port': 'فایل_انتقال_شماره_درگاه', 'args': 'آرگومان_آرايه', 'server': 'سرور_مقدار', 'data': 'داده_ها', 'ethernet_input': '이더넷입력', 'trace_packet': 'اثر_ماتریس_بسته', 'GATEWAY': '관문기계주소', 'rule': 'فیلتر_مقدار', 'protocol': '통신규약', 'forwards': '전달규칙들', 'occupied': '사용중주소', 'host': 'میزبان', 'ack': '확인번호', 'serial_port': '직렬접속번호', 'readers': '읽기대상들', 'guest': 'مهمان', 'destination': 'مقصد_داده_ها_آدرس', 'ethernet_port': 'درگاه_اِترنت', 'b': '둘째값', 'MAC': 'دستگاه_آدرس', 'arp': 'آدرس_دقت_بسته', 'writable': '쓸수있음', 'direction': '방향', 'seq': '순서번호', 'frame': '실행틀', 'loop': 'چرخه_مقدار', 'port': 'شماره_درگاه', 'offset': 'جابجایی_لایه_ای_مقدار', 'readable': '읽을수있음', 'c': 'کد_نویسه', 'p': 'داده_ها_مرتب_کردن', 'writers': '쓰기대상들', 'IP': 'آدرس_اینترنتی_مقدار', 'e': '보조항목', 'n': '개수', 'packet': 'بسته_داده_ها', 'arguments': '전달인수', 'source': '원본자료', 'NetworkBridge': 'شبکه_پل', 'window': 'پنجره', 'capture': 'ضبط_کردن'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
