#!/usr/bin/env python3
"""기존 راستہ_2 호환 اندراج_نقطہ. اصل_کوائف 구현: ../ٹولز/파일전송시험.py"""
import importlib as 가져오기
import sys as آپریٹنگ_سسٹم_قدر
from pathlib import Path as راستہ_2
آپریٹنگ_سسٹم_قدر.path.insert(0, str(راستہ_2(__file__).resolve().parents[1] / 'ٹولز'))
if __name__ == '__main__':
    import runpy as ایپ_ایپ_دراز
    ایپ_ایپ_دراز.run_module('파일전송시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('파일전송시험')
    대응 = {'timeout': '시간제한', 'payload': 'پے_لوڈ_کوائف', 'broken': '손상자료', 'linux_example': '리눅스예제', 'chunk': '조각', 'data': 'کوائف', 'proc': 'عمل_کاری', 'code': '명령열', 'linux': '리눅스파일', 'archive': 'محفوظ', 'main': 'چلائیں', 'net_source': '통신원문', 'temporary': '임시자원', 'static_source': 'جامد_ماخذ', 'java_source': '자바원문', 'echo': '되돌림서버항목', 'ROOT': 'عکس_ڈالنا_روٹ', 'text': 'متن', 'marker': '확인표시', 'EchoFixture': '되돌림시험서버', 'command': 'حکم', 'out': 'پیمائش_کوائف', 'expected': '예상결과', 'server_source': 'سرور_ماخذ', 'shell': 'شیل', 'upload': 'اپ_لوڈ_کريں_فائلیں', 'transcript': '대화기록', 'port': 'دہانہ_نمبر', 'native': '자체실행파일', 'elf': '실행파일', 'server_udp_port': '서버전문접속번호', 'packed': '묶인자료', 'bridge': 'برج', 'selector': 'منتخب_کنندہ', 'end': 'اختتام_آفسٹ', 'e': '보조항목', 'ftp': 'فائل_منتقلی_رابطہ', 'key': '누름값', 'bytecode': '바이트코드', 'peer': 'ساتھی_قدر', 'result': 'پیمائش', 'unchanged': '보존자료', 'line': 'اندراج_کی_سطر', 'server_tcp_port': 'سرور_بہاؤ_پورٹ', 'source': '원본자료', 'NetworkBridge': 'نیٹ_ورک_برج', 'jar': '자바꾸러미', 'receive': '수신하기', 'report': 'توثیق_رپورٹ'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
