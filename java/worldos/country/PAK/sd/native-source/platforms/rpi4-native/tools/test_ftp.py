#!/usr/bin/env python3
"""기존 راههه 호환 داخلا_هنڌ. اصلي_ڪوائف 구현: ../اوزار/파일전송시험.py"""
import importlib as 가져오기
import sys as آپريٽنگ_سسٽم_قدر
from pathlib import Path as راههه
آپريٽنگ_سسٽم_قدر.path.insert(0, str(راههه(__file__).resolve().parents[1] / 'اوزار'))
if __name__ == '__main__':
    import runpy as ائپ_ائپ_ڊرائر
    ائپ_ائپ_ڊرائر.run_module('파일전송시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('파일전송시험')
    대응 = {'timeout': '시간제한', 'payload': 'بنيادي_بار_ڪوائف', 'broken': '손상자료', 'linux_example': '리눅스예제', 'chunk': '조각', 'data': 'ڪوائف', 'proc': 'عمل_a7054519', 'code': 'هدايت_ترتيب', 'linux': '리눅스파일', 'archive': 'محفوظ', 'main': 'هلائڻ', 'net_source': '통신원문', 'temporary': '임시자원', 'static_source': 'ساقط_ماخذ', 'java_source': '자바원문', 'echo': '되돌림서버항목', 'ROOT': '기준', 'text': 'متن', 'marker': '확인표시', 'EchoFixture': '되돌림시험서버', 'command': 'حڪم', 'out': '결과자료', 'expected': '예상결과', 'server_source': 'سرور_ماخذ', 'shell': 'شيل', 'upload': 'اپ_لوڊ_ڪريو_فائلون', 'transcript': '대화기록', 'port': '접속번호', 'native': '자체실행파일', 'elf': '실행파일', 'server_udp_port': '서버전문접속번호', 'packed': '묶인자료', 'bridge': '연결다리', 'selector': 'چونڊيندڙ', 'end': 'ختم_ڪريو_آف_سيٽ', 'e': '보조항목', 'ftp': 'فائل_منتقلي_ڪنيڪشن', 'key': '누름값', 'bytecode': '바이트코드', 'peer': 'همعصر_قدر', 'result': '결과', 'unchanged': '보존자료', 'line': 'لڪير', 'server_tcp_port': 'سرور_اسٽريم_پورٽ', 'source': '원본자료', 'NetworkBridge': '통신다리', 'jar': '자바꾸러미', 'receive': '수신하기', 'report': 'ڪارگر_رپورٽ'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
