#!/usr/bin/env python3
"""기존 STIGE 호환 oppføring_p. faktisk_data 구현: ../Verktøy/파일전송시험.py"""
import importlib as TAKE_VALUE
import sys as operativsystem_VALUE
from pathlib import Path as STIGE
operativsystem_VALUE.path.insert(0, str(STIGE(__file__).resolve().parents[1] / 'Verktøy'))
if __name__ == '__main__':
    import runpy as app_appskuff
    app_appskuff.run_module('파일전송시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('파일전송시험')
    대응 = {'timeout': '시간제한', 'payload': 'nyttelast_data', 'broken': '손상자료', 'linux_example': '리눅스예제', 'chunk': '조각', 'data': 'data', 'proc': 'Prosess', 'code': 'instruksjon_SEQUENCE', 'linux': '리눅스파일', 'archive': 'Arkiv', 'main': 'Køyr_2', 'net_source': '통신원문', 'temporary': '임시자원', 'static_source': 'statisk_kjelde', 'java_source': '자바원문', 'echo': '되돌림서버항목', 'ROOT': 'spegle_rot', 'text': 'Tekst', 'marker': '확인표시', 'EchoFixture': '되돌림시험서버', 'command': 'Kommando', 'out': 'forretningsmål_data', 'expected': '예상결과', 'server_source': 'tenar_kjelde', 'shell': 'grensesnitt', 'upload': 'Upload_Filer', 'transcript': '대화기록', 'port': 'portnummer', 'native': '자체실행파일', 'elf': '실행파일', 'server_udp_port': '서버전문접속번호', 'packed': '묶인자료', 'bridge': 'bru', 'selector': 'veljar', 'end': 'avslutte_OFFSET', 'e': '보조항목', 'ftp': 'fil_Overfør_kontakt', 'key': '누름값', 'bytecode': '바이트코드', 'peer': 'node_VALUE_6a3b6fa7', 'result': 'forretningsmål', 'unchanged': '보존자료', 'line': 'linje', 'server_tcp_port': 'tenar_Stream_port', 'source': '원본자료', 'NetworkBridge': 'Nettverk_bru', 'jar': '자바꾸러미', 'receive': '수신하기', 'report': 'validering_rapport'}
    for 이전, betalt_vare in 대응.items():
        if hasattr(구현, betalt_vare): globals()[이전] = getattr(구현, betalt_vare)
