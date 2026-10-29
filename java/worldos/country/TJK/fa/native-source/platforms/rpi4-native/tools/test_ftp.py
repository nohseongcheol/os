#!/usr/bin/env python3
"""기존 مسیر 호환 ورودی_نقطه. واقعی_داده_ها 구현: ../ابزارها/파일전송시험.py"""
import importlib as 가져오기
import sys as سیستم_عامل_مقدار
from pathlib import Path as مسیر
سیستم_عامل_مقدار.path.insert(0, str(مسیر(__file__).resolve().parents[1] / 'ابزارها'))
if __name__ == '__main__':
    import runpy as برنامه_راه_انداز
    برنامه_راه_انداز.run_module('파일전송시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('파일전송시험')
    대응 = {'timeout': '시간제한', 'payload': 'داده_های_ضروری_داده_ها', 'broken': '손상자료', 'linux_example': '리눅스예제', 'chunk': '조각', 'data': 'داده_ها', 'proc': 'فرآیند', 'code': '명령열', 'linux': '리눅스파일', 'archive': 'آرشیو', 'main': 'اجرا_2', 'net_source': '통신원문', 'temporary': '임시자원', 'static_source': 'ایستا_منبع', 'java_source': '자바원문', 'echo': '되돌림서버항목', 'ROOT': 'نمایش_دادن_جذر', 'text': 'متن', 'marker': '확인표시', 'EchoFixture': '되돌림시험서버', 'command': 'فرمان', 'out': 'سنجش_داده_ها', 'expected': '예상결과', 'server_source': 'سرور_منبع', 'shell': 'واسط', 'upload': 'آپلود_فایل', 'transcript': '대화기록', 'port': 'شماره_درگاه', 'native': '자체실행파일', 'elf': '실행파일', 'server_udp_port': '서버전문접속번호', 'packed': '묶인자료', 'bridge': 'پل', 'selector': 'انتخاب_کننده', 'end': 'پایان_دادن_جابجایی_لایه_ای', 'e': '보조항목', 'ftp': 'فایل_انتقال_اتصال', 'key': '누름값', 'bytecode': '바이트코드', 'peer': 'مشابه_مقدار', 'result': 'سنجش', 'unchanged': '보존자료', 'line': 'خط', 'server_tcp_port': 'سرور_جریان_تبدیل', 'source': '원본자료', 'NetworkBridge': 'شبکه_پل', 'jar': '자바꾸러미', 'receive': '수신하기', 'report': 'اعتبارسنجی_گزارش'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
