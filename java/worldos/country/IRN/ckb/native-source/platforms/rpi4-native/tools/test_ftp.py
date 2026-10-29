#!/usr/bin/env python3
"""기존 گوزەر 호환 تێنووسین_خاڵ. ڕاستەکی_دەیتا 구현: ../ئامرازەکان/파일전송시험.py"""
import importlib as 가져오기
import sys as سیستەمی_کارپێکردن_نرخ
from pathlib import Path as گوزەر
سیستەمی_کارپێکردن_نرخ.path.insert(0, str(گوزەر(__file__).resolve().parents[1] / 'ئامرازەکان'))
if __name__ == '__main__':
    import runpy as بەرنامە_ئەندامی_ستاف
    بەرنامە_ئەندامی_ستاف.run_module('파일전송시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('파일전송시험')
    대응 = {'timeout': '시간제한', 'payload': 'بارگەى_كرێ_دەیتا', 'broken': '손상자료', 'linux_example': '리눅스예제', 'chunk': '조각', 'data': 'دەیتا', 'proc': 'پرۆسە', 'code': 'ڕێنمایی_زنجیره', 'linux': '리눅스파일', 'archive': 'ئەرشیف', 'main': 'ڕادان', 'net_source': '통신원문', 'temporary': '임시자원', 'static_source': 'ستاتیک_ژێدەر', 'java_source': '자바원문', 'echo': '되돌림서버항목', 'ROOT': '기준', 'text': 'دەق', 'marker': '확인표시', 'EchoFixture': '되돌림시험서버', 'command': 'فەرمان', 'out': '결과자료', 'expected': '예상결과', 'server_source': 'ڕاژەکار_ژێدەر', 'shell': 'توێکڵ', 'upload': 'بار_کردن_فایله_کان', 'transcript': '대화기록', 'port': '접속번호', 'native': '자체실행파일', 'elf': '실행파일', 'server_udp_port': '서버전문접속번호', 'packed': '묶인자료', 'bridge': '연결다리', 'selector': 'هەڵبژێرەر', 'end': 'دوایی_کردن_ئۆفسێت', 'e': '보조항목', 'ftp': 'فایل_گواستنەوە_گرێدان', 'key': '누름값', 'bytecode': '바이트코드', 'peer': 'هاوتا_نرخ', 'result': '결과', 'unchanged': '보존자료', 'line': 'دێڕ', 'server_tcp_port': 'ڕاژەکار_Stream_دەرگا', 'source': '원본자료', 'NetworkBridge': '통신다리', 'jar': '자바꾸러미', 'receive': '수신하기', 'report': 'ڕەواکردن_ڕاپۆرت'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
