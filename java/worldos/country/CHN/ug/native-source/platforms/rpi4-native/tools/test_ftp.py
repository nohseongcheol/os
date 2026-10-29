#!/usr/bin/env python3
"""기존 يول 호환 كىرگۈزۈش_نوقتا. ھەقىقىي_مەلۇمات 구현: ../قوراللار/파일전송시험.py"""
import importlib as 가져오기
import sys as مەشغۇلات_سىستېمىسى_قىممىتى
from pathlib import Path as يول
مەشغۇلات_سىستېمىسى_قىممىتى.path.insert(0, str(يول(__file__).resolve().parents[1] / 'قوراللار'))
if __name__ == '__main__':
    import runpy as ئەپ_خادىم
    ئەپ_خادىم.run_module('파일전송시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('파일전송시험')
    대응 = {'timeout': '시간제한', 'payload': 'يۈك_مەلۇمات', 'broken': '손상자료', 'linux_example': '리눅스예제', 'chunk': '조각', 'data': 'مەلۇمات', 'proc': 'جەريان', 'code': '명령열', 'linux': '리눅스파일', 'archive': 'ئارخىپ', 'main': 'ئىجرا_قىل_2', 'net_source': '통신원문', 'temporary': '임시자원', 'static_source': 'ئىستاتىك_مەنبە', 'java_source': '자바원문', 'echo': '되돌림서버항목', 'ROOT': 'كۆرسىتىش_يىلتىز', 'text': 'تېكىست', 'marker': '확인표시', 'EchoFixture': '되돌림시험서버', 'command': 'بۇيرۇق', 'out': 'ئۆلچەم_مەلۇمات', 'expected': '예상결과', 'server_source': 'مۇلازىمىتېر_مەنبە', 'shell': 'قاپ', 'upload': 'يۈكلىمەك_ھۆججەت', 'transcript': '대화기록', 'port': '접속번호', 'native': '자체실행파일', 'elf': '실행파일', 'server_udp_port': '서버전문접속번호', 'packed': '묶인자료', 'bridge': 'كۆۋرۈك', 'selector': 'تاللىغۇچ', 'end': 'تاماملىماق_ئاغما', 'e': '보조항목', 'ftp': 'ھۆججەت_يوللاش_ئۇلىنىش', 'key': '누름값', 'bytecode': '바이트코드', 'peer': 'باراۋەرلىك_قىممىتى', 'result': 'ئۆلچەم', 'unchanged': '보존자료', 'line': 'قۇر', 'server_tcp_port': 'مۇلازىمىتېر_ئېقىم_ئېغىز', 'source': '원본자료', 'NetworkBridge': 'تور_كۆۋرۈك', 'jar': '자바꾸러미', 'receive': '수신하기', 'report': 'دەلىللەش_خەۋەر'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
