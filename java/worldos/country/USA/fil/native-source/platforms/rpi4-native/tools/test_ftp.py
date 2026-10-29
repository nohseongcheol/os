#!/usr/bin/env python3
"""기존 path 호환 pagpasok_point. totoo_data 구현: ../Mga_Tool/파일전송시험.py"""
import importlib as TAKE_VALUE
import sys as operating_system_VALUE
from pathlib import Path as path
operating_system_VALUE.path.insert(0, str(path(__file__).resolve().parents[1] / 'Mga_Tool'))
if __name__ == '__main__':
    import runpy as app_launcher
    app_launcher.run_module('파일전송시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('파일전송시험')
    대응 = {'timeout': '시간제한', 'payload': 'payload_data', 'broken': '손상자료', 'linux_example': '리눅스예제', 'chunk': '조각', 'data': 'data', 'proc': 'Proseso', 'code': 'instruksiyon_SEQUENCE', 'linux': '리눅스파일', 'archive': 'Archive', 'main': 'run', 'net_source': '통신원문', 'temporary': '임시자원', 'static_source': 'hindi_nababago_pinagmulan', 'java_source': '자바원문', 'echo': '되돌림서버항목', 'ROOT': 'Project_root', 'text': 'SMS', 'marker': '확인표시', 'EchoFixture': '되돌림시험서버', 'command': 'utos', 'out': 'sukat_data', 'expected': '예상결과', 'server_source': 'server_pinagmulan', 'shell': 'shell', 'upload': 'upload_Mga_File', 'transcript': '대화기록', 'port': 'numero_ng_port', 'native': '자체실행파일', 'elf': '실행파일', 'server_udp_port': '서버전문접속번호', 'packed': '묶인자료', 'bridge': 'bridge', 'selector': 'tagapili', 'end': 'tapusin_OFFSET', 'e': '보조항목', 'ftp': 'file_lipat_koneksyon', 'key': '누름값', 'bytecode': '바이트코드', 'peer': 'peer_VALUE', 'result': 'sukat', 'unchanged': '보존자료', 'line': 'linya', 'server_tcp_port': 'server_Stream_port', 'source': '원본자료', 'NetworkBridge': 'Network_bridge', 'jar': '자바꾸러미', 'receive': '수신하기', 'report': 'pagpapatibay_ulat'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
