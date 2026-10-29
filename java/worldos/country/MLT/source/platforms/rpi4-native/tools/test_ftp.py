#!/usr/bin/env python3
"""기존 mogħdija 호환 entrata_punt. attwali_data 구현: ../Għodod/파일전송시험.py"""
import importlib as TAKE_VALUE
import sys as sistema_operattiva_VALUE
from pathlib import Path as mogħdija
sistema_operattiva_VALUE.path.insert(0, str(mogħdija(__file__).resolve().parents[1] / 'Għodod'))
if __name__ == '__main__':
    import runpy as programm_ġabra_ta_apps
    programm_ġabra_ta_apps.run_module('파일전송시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('파일전송시험')
    대응 = {'timeout': '시간제한', 'payload': 'payload_data', 'broken': '손상자료', 'linux_example': '리눅스예제', 'chunk': '조각', 'data': 'data', 'proc': 'Proċess', 'code': 'istruzzjoni_SEQUENCE', 'linux': '리눅스파일', 'archive': 'Arkivju', 'main': 'serje', 'net_source': '통신원문', 'temporary': '임시자원', 'static_source': 'statiku_sors', 'java_source': '자바원문', 'echo': '되돌림서버항목', 'ROOT': 'pprojetta_għerq', 'text': 'SMS', 'marker': '확인표시', 'EchoFixture': '되돌림시험서버', 'command': 'kmand', 'out': 'miżura_data', 'expected': '예상결과', 'server_source': 'server_sors', 'shell': 'shell', 'upload': 'tella_Fajls', 'transcript': '대화기록', 'port': '접속번호', 'native': '자체실행파일', 'elf': '실행파일', 'server_udp_port': '서버전문접속번호', 'packed': '묶인자료', 'bridge': 'pont', 'selector': 'selettur', 'end': 'ttermina_OFFSET', 'e': '보조항목', 'ftp': 'fajl_trasferiment_konnessjoni', 'key': '누름값', 'bytecode': '바이트코드', 'peer': 'peer_VALUE', 'result': 'miżura', 'unchanged': '보존자료', 'line': 'linja', 'server_tcp_port': 'server_Stream_port', 'source': '원본자료', 'NetworkBridge': 'netwerk_pont', 'jar': '자바꾸러미', 'receive': '수신하기', 'report': 'validazzjoni_rapport'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
