#!/usr/bin/env python3
"""기존 راستہ_2 호환 اندراج_نقطہ. اصل_کوائف 구현: ../ٹولز/نیٹ_ورک_برج.py"""
import importlib as 가져오기
import sys as آپریٹنگ_سسٹم_قدر
from pathlib import Path as راستہ_2
آپریٹنگ_سسٹم_قدر.path.insert(0, str(راستہ_2(__file__).resolve().parents[1] / 'ٹولز'))
if __name__ == '__main__':
    import runpy as ایپ_ایپ_دراز
    ایپ_ایپ_دراز.run_module('نیٹ_ورک_برج', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('نیٹ_ورک_برج')
    대응 = {'response': '응답자료', 'parts': 'راہ_جزو', 's': 'سلک_کوائف', 'i': '순번', 'close': 'بند_کریں', 'forward': '전달규칙', 'slip_input': '직렬전문입력', 'self': '자신', 'item': 'اندراج_قدر', 'flags': '설정비트', 'ftp_port': 'فائل_منتقلی_دہانہ_نمبر', 'args': 'دلائل_لڑی', 'server': 'سرور_قدر', 'data': 'کوائف', 'ethernet_input': '이더넷입력', 'trace_packet': 'ٹریس_پیکٹ', 'GATEWAY': '관문기계주소', 'rule': 'فلٹر_قدر', 'protocol': '통신규약', 'forwards': '전달규칙들', 'occupied': '사용중주소', 'host': 'میزبان', 'ack': '확인번호', 'serial_port': '직렬접속번호', 'readers': '읽기대상들', 'guest': 'مہمان', 'destination': 'منزل_مقصود_کوائف_پتہ', 'ethernet_port': 'ایتھرنیٹ_پورٹ', 'b': '둘째값', 'MAC': 'مشین_پتہ', 'arp': 'پتہ_جزیات_کاری_پیکٹ', 'writable': '쓸수있음', 'direction': '방향', 'seq': '순서번호', 'frame': '실행틀', 'loop': 'گردش_قدر', 'port': 'دہانہ_نمبر', 'offset': 'آفسٹ_قدر', 'readable': '읽을수있음', 'c': 'کریکٹر_ضابطہ', 'p': 'کوائف_پوزیشن_ٹھیک_کریں', 'writers': '쓰기대상들', 'IP': 'انٹرنیٹ_پتہ_قدر', 'e': '보조항목', 'n': '개수', 'packet': 'پیکٹ_کوائف', 'arguments': '전달인수', 'source': '원본자료', 'NetworkBridge': 'نیٹ_ورک_برج', 'window': 'ونڈو', 'capture': 'کیپچر_کریں'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
