#!/usr/bin/env python3
"""기존 પથ 호환 પ્રવેશ_બિંદુ. વાસ્તવિક_ડેટા 구현: ../ઉપકરણો/파일전송시험.py"""
import importlib as 가져오기
import sys as ઑપરેટિંગ_સિસ્ટમ_મૂલ્ય
from pathlib import Path as પથ
ઑપરેટિંગ_સિસ્ટમ_મૂલ્ય.path.insert(0, str(પથ(__file__).resolve().parents[1] / 'ઉપકરણો'))
if __name__ == '__main__':
    import runpy as એપ્લિકેશન_લૉન્ચર
    એપ્લિકેશન_લૉન્ચર.run_module('파일전송시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('파일전송시험')
    대응 = {'timeout': '시간제한', 'payload': 'પેલોડ_ડેટા', 'broken': '손상자료', 'linux_example': '리눅스예제', 'chunk': '조각', 'data': 'ડેટા', 'proc': 'પ્રક્રિયા', 'code': '명령열', 'linux': '리눅스파일', 'archive': 'સંગ્રહ', 'main': 'ચલાવો_2', 'net_source': '통신원문', 'temporary': '임시자원', 'static_source': 'સ્થિર_સ્રોત', 'java_source': '자바원문', 'echo': '되돌림서버항목', 'ROOT': 'પ્રોજેક્ટ_રૂટ', 'text': 'લખાણ', 'marker': '확인표시', 'EchoFixture': '되돌림시험서버', 'command': 'આદેશ', 'out': 'પરિમાણ_ડેટા', 'expected': '예상결과', 'server_source': 'સર્વર_સ્રોત', 'shell': 'શેલ', 'upload': 'અપલોડ_કરો_ફાઇલો', 'transcript': '대화기록', 'port': 'પોર્ટ_નંબર', 'native': '자체실행파일', 'elf': '실행파일', 'server_udp_port': '서버전문접속번호', 'packed': '묶인자료', 'bridge': 'બ્રિજ', 'selector': 'પસંદકર્તા', 'end': 'અંત_કરો_ઑફસેટ', 'e': '보조항목', 'ftp': 'ફાઇલ_સ્થાનાંતર_કનેક્શન', 'key': '누름값', 'bytecode': '바이트코드', 'peer': 'પીઅર_મૂલ્ય', 'result': 'પરિમાણ', 'unchanged': '보존자료', 'line': 'લાઇન', 'server_tcp_port': 'સર્વર_સ્ટ્રીમ_પૉર્ટ', 'source': '원본자료', 'NetworkBridge': 'નેટવર્ક_બ્રિજ', 'jar': '자바꾸러미', 'receive': '수신하기', 'report': 'માન્યતા_અહેવાલ'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
