#!/usr/bin/env python3
"""기존 பாதை_2 호환 நுழைவுப்_புள்ளி. அசல்_தரவு 구현: ../கருவிகள்/파일전송시험.py"""
import importlib as 가져오기
import sys as இயக்க_முறைமை_மதிப்பு
from pathlib import Path as பாதை_2
இயக்க_முறைமை_மதிப்பு.path.insert(0, str(பாதை_2(__file__).resolve().parents[1] / 'கருவிகள்'))
if __name__ == '__main__':
    import runpy as நிரல்_துவக்குநர்
    நிரல்_துவக்குநர்.run_module('파일전송시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('파일전송시험')
    대응 = {'timeout': '시간제한', 'payload': 'பேலோட்_தரவு', 'broken': '손상자료', 'linux_example': '리눅스예제', 'chunk': '조각', 'data': 'தரவு', 'proc': 'செயல்பாடு', 'code': '명령열', 'linux': '리눅스파일', 'archive': 'காப்பகம்', 'main': 'செயல்படுத்துக', 'net_source': '통신원문', 'temporary': '임시자원', 'static_source': 'மாறா_மூலம்', 'java_source': '자바원문', 'echo': '되돌림서버항목', 'ROOT': 'திட்டப்பணி_மூலம்', 'text': 'உரை', 'marker': '확인표시', 'EchoFixture': '되돌림시험서버', 'command': 'கட்டளை', 'out': 'அளவிடக்கூடியது_தரவு', 'expected': '예상결과', 'server_source': 'சேவையகம்_மூலம்', 'shell': 'கூடு', 'upload': 'பதிவேற்று_கோப்புகள்', 'transcript': '대화기록', 'port': 'முனைய_எண்', 'native': '자체실행파일', 'elf': 'செயல்படுத்தக்கூடிய_கோப்பு', 'server_udp_port': '서버전문접속번호', 'packed': '묶인자료', 'bridge': 'பிரிட்ஜ்', 'selector': 'தேர்வி', 'end': 'முடி_ஆஃப்செட்', 'e': '보조항목', 'ftp': 'கோப்பு_இடமாற்று_இணைப்பு', 'key': '누름값', 'bytecode': '바이트코드', 'peer': 'பியர்_மதிப்பு', 'result': 'அளவிடக்கூடியது', 'unchanged': '보존자료', 'line': 'உள்ளீட்டு_வரி', 'server_tcp_port': 'சேவையகம்_தொடரோடி_முணையம்', 'source': '원본자료', 'NetworkBridge': 'பிணையம்_பிரிட்ஜ்', 'jar': '자바꾸러미', 'receive': '수신하기', 'report': 'செல்லுபடியாக்கம்_அறிக்கை'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
