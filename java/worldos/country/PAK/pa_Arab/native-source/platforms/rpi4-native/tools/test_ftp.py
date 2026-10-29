#!/usr/bin/env python3
"""기존 راہ 호환 داخلہ_مقام. اصلی_کوائف 구현: ../اوزار/파일전송시험.py"""
import importlib as 가져오기
import sys as آپریٹنگ_سسٹم_قدر
from pathlib import Path as راہ
آپریٹنگ_سسٹم_قدر.path.insert(0, str(راہ(__file__).resolve().parents[1] / 'اوزار'))
if __name__ == '__main__':
    import runpy as ایپ_عملے_دا_رکن
    ایپ_عملے_دا_رکن.run_module('파일전송시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('파일전송시험')
    대응 = {'timeout': '시간제한', 'payload': 'پے_لوڈ_کوائف', 'broken': '손상자료', 'linux_example': '리눅스예제', 'chunk': '조각', 'data': 'کوائف', 'proc': 'عمل', 'code': '명령열', 'linux': '리눅스파일', 'archive': 'محفوظہ', 'main': 'چلاؤ', 'net_source': '통신원문', 'temporary': '임시자원', 'static_source': 'ساقط_ماخذ', 'java_source': '자바원문', 'echo': '되돌림서버항목', 'ROOT': '기준', 'text': 'متن', 'marker': '확인표시', 'EchoFixture': '되돌림시험서버', 'command': 'حکم', 'out': '결과자료', 'expected': '예상결과', 'server_source': 'سرور_ماخذ', 'shell': 'شیل', 'upload': 'اپ_لوڈ_کرو_فائلاں', 'transcript': '대화기록', 'port': '접속번호', 'native': '자체실행파일', 'elf': '실행파일', 'server_udp_port': '서버전문접속번호', 'packed': '묶인자료', 'bridge': 'برج', 'selector': 'منتخب_کرنڑ_آلا', 'end': 'ختم_کرو_آف_سیٹ', 'e': '보조항목', 'ftp': 'فائل_منتقلی_کنکشن', 'key': '누름값', 'bytecode': '바이트코드', 'peer': 'ہم_سر_قدر', 'result': '결과', 'unchanged': '보존자료', 'line': 'لائن', 'server_tcp_port': 'سرور_سٹریم_دہانہ', 'source': '원본자료', 'NetworkBridge': 'نیٹ_ورک_برج', 'jar': '자바꾸러미', 'receive': '수신하기', 'report': 'جواز_دہی_رپورٹ'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
