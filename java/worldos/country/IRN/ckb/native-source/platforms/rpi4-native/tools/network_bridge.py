#!/usr/bin/env python3
"""기존 گوزەر 호환 تێنووسین_خاڵ. ڕاستەکی_دەیتا 구현: ../ئامرازەکان/통신다리.py"""
import importlib as 가져오기
import sys as سیستەمی_کارپێکردن_نرخ
from pathlib import Path as گوزەر
سیستەمی_کارپێکردن_نرخ.path.insert(0, str(گوزەر(__file__).resolve().parents[1] / 'ئامرازەکان'))
if __name__ == '__main__':
    import runpy as بەرنامە_ئەندامی_ستاف
    بەرنامە_ئەندامی_ستاف.run_module('통신다리', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('통신다리')
    대응 = {'response': '응답자료', 'parts': 'گوزەر_پارچە', 's': 'رست_دەیتا', 'i': '순번', 'close': 'داخستن', 'forward': '전달규칙', 'slip_input': '직렬전문입력', 'self': '자신', 'item': 'تێنووسین_نرخ', 'flags': '설정비트', 'ftp_port': '파일전송접속번호', 'args': 'ئارگیومێنت_ڕیزی_داتا', 'server': 'ڕاژەکار_نرخ', 'data': 'دەیتا', 'ethernet_input': '이더넷입력', 'trace_packet': '전문추적', 'GATEWAY': '관문기계주소', 'rule': 'ڕێسا_نرخ', 'protocol': '통신규약', 'forwards': '전달규칙들', 'occupied': '사용중주소', 'host': 'جێدەر', 'ack': '확인번호', 'serial_port': '직렬접속번호', 'readers': '읽기대상들', 'guest': '커널실행', 'destination': 'جێمەبەست_دەیتا_ناونیشان', 'ethernet_port': 'ئێتێرنێت_دەرگا', 'b': '둘째값', 'MAC': 'مەکینه_ناونیشان', 'arp': 'ناونیشان_وردبینی_پاکه_ت', 'writable': '쓸수있음', 'direction': '방향', 'seq': '순서번호', 'frame': '실행틀', 'loop': 'خول_نرخ', 'port': '접속번호', 'offset': 'ئۆفسێت_نرخ', 'readable': '읽을수있음', 'c': 'کۆدی_نووسە', 'p': '자료위치', 'writers': '쓰기대상들', 'IP': 'ناونیشانی_ئینتەرنێتی_نرخ', 'e': '보조항목', 'n': '개수', 'packet': 'پاکه_ت_دەیتا', 'arguments': '전달인수', 'source': '원본자료', 'NetworkBridge': '통신다리', 'window': 'پەنجەرە', 'capture': 'تۆمارکردن'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
