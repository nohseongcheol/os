#!/usr/bin/env python3
"""기존 راہ 호환 داخلہ_مقام. اصلی_کوائف 구현: ../اوزار/نیٹ_ورک_برج.py"""
import importlib as 가져오기
import sys as آپریٹنگ_سسٹم_قدر
from pathlib import Path as راہ
آپریٹنگ_سسٹم_قدر.path.insert(0, str(راہ(__file__).resolve().parents[1] / 'اوزار'))
if __name__ == '__main__':
    import runpy as ایپ_عملے_دا_رکن
    ایپ_عملے_دا_رکن.run_module('نیٹ_ورک_برج', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('نیٹ_ورک_برج')
    대응 = {'response': '응답자료', 'parts': 'راہ_جزو', 's': 'سٹرنگ_کوائف', 'i': '순번', 'close': 'بند_کرو', 'forward': '전달규칙', 'slip_input': '직렬전문입력', 'self': '자신', 'item': 'داخلہ_قدر', 'flags': '설정비트', 'ftp_port': '파일전송접속번호', 'args': 'دلیل_ایرے', 'server': 'سرور_قدر', 'data': 'کوائف', 'ethernet_input': '이더넷입력', 'trace_packet': '전문추적', 'GATEWAY': '관문기계주소', 'rule': 'فلٹر_قدر', 'protocol': '통신규약', 'forwards': '전달규칙들', 'occupied': '사용중주소', 'host': 'مہمان_b78e430d', 'ack': '확인번호', 'serial_port': '직렬접속번호', 'readers': '읽기대상들', 'guest': 'مہمان', 'destination': 'منزل_مقصود_کوائف_پتا', 'ethernet_port': 'ایتھرنیٹ_دہانہ', 'b': '둘째값', 'MAC': 'مشین_پتا', 'arp': 'پتا_جزیات_کاری_پیکٹ', 'writable': '쓸수있음', 'direction': '방향', 'seq': '순서번호', 'frame': '실행틀', 'loop': 'دورہ_قدر', 'port': '접속번호', 'offset': 'آف_سیٹ_قدر', 'readable': '읽을수있음', 'c': 'کیریکٹر_کوڈ', 'p': '자료위치', 'writers': '쓰기대상들', 'IP': 'انٹرنیٹ_پتا_قدر', 'e': '보조항목', 'n': '개수', 'packet': 'پیکٹ_کوائف', 'arguments': '전달인수', 'source': '원본자료', 'NetworkBridge': 'نیٹ_ورک_برج', 'window': 'کھڑکی', 'capture': 'کھیچو'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
