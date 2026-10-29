#!/usr/bin/env python3
"""기존 راههه 호환 داخلا_هنڌ. اصلي_ڪوائف 구현: ../اوزار/통신다리.py"""
import importlib as 가져오기
import sys as آپريٽنگ_سسٽم_قدر
from pathlib import Path as راههه
آپريٽنگ_سسٽم_قدر.path.insert(0, str(راههه(__file__).resolve().parents[1] / 'اوزار'))
if __name__ == '__main__':
    import runpy as ائپ_ائپ_ڊرائر
    ائپ_ائپ_ڊرائر.run_module('통신다리', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('통신다리')
    대응 = {'response': '응답자료', 'parts': 'راههه_جز', 's': 'اسٽرنگ_ڪوائف', 'i': '순번', 'close': 'بند_ڪرڻ', 'forward': '전달규칙', 'slip_input': '직렬전문입력', 'self': '자신', 'item': 'داخلا_قدر', 'flags': '설정비트', 'ftp_port': '파일전송접속번호', 'args': 'دليل_ترتيب', 'server': 'سرور_قدر', 'data': 'ڪوائف', 'ethernet_input': '이더넷입력', 'trace_packet': '전문추적', 'GATEWAY': '관문기계주소', 'rule': 'فلٽر_قدر', 'protocol': '통신규약', 'forwards': '전달규칙들', 'occupied': '사용중주소', 'host': 'مهمان', 'ack': '확인번호', 'serial_port': '직렬접속번호', 'readers': '읽기대상들', 'guest': '커널실행', 'destination': 'منزل_مقصود_ڪوائف_پتو', 'ethernet_port': 'ايٿرنيٽ_پورٽ', 'b': '둘째값', 'MAC': 'مشين_پتو', 'arp': '주소찾기전문', 'writable': '쓸수있음', 'direction': '방향', 'seq': '순서번호', 'frame': '실행틀', 'loop': 'ڦيرو_قدر', 'port': '접속번호', 'offset': 'آف_سيٽ_قدر', 'readable': '읽을수있음', 'c': 'ڪئريڪٽر_ڪوڊ', 'p': '자료위치', 'writers': '쓰기대상들', 'IP': 'انٽرنيٽ_پتو_قدر', 'e': '보조항목', 'n': '개수', 'packet': '꾸러미자료', 'arguments': '전달인수', 'source': '원본자료', 'NetworkBridge': '통신다리', 'window': 'دري', 'capture': 'ڪيپچر'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
