#!/usr/bin/env python3
"""기존 Wee 호환 Agab_Punkt. aktuell_Daten 구현: ../Tools/파일전송시험.py"""
import importlib as TAKE_VALUE
import sys as Betribssystem_VALUE
from pathlib import Path as Wee
Betribssystem_VALUE.path.insert(0, str(Wee(__file__).resolve().parents[1] / 'Tools'))
if __name__ == '__main__':
    import runpy as App_App_Beräich
    App_App_Beräich.run_module('파일전송시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('파일전송시험')
    대응 = {'timeout': '시간제한', 'payload': 'nëtzlech_Charge_Daten', 'broken': '손상자료', 'linux_example': '리눅스예제', 'chunk': '조각', 'data': 'Daten', 'proc': 'Prozess', 'code': 'Instruktioun_SEQUENCE', 'linux': '리눅스파일', 'archive': 'Archiv', 'main': 'Laf', 'net_source': '통신원문', 'temporary': '임시자원', 'static_source': 'statesch_Quell', 'java_source': '자바원문', 'echo': '되돌림서버항목', 'ROOT': 'projezéieren_Racinn', 'text': 'SMS', 'marker': 'Markéierung', 'EchoFixture': '되돌림시험서버', 'command': 'Befeel', 'out': 'Mooss_Daten', 'expected': '예상결과', 'server_source': 'Server_Quell', 'shell': 'Shell', 'upload': 'eroplueden_Fichieren', 'transcript': '대화기록', 'port': '접속번호', 'native': '자체실행파일', 'elf': '실행파일', 'server_udp_port': '서버전문접속번호', 'packed': '묶인자료', 'bridge': 'Bréck', 'selector': 'Selekteur', 'end': 'bëennegen_OFFSET', 'e': '보조항목', 'ftp': 'Fichier_Transfer_Verbindung', 'key': '누름값', 'bytecode': '바이트코드', 'peer': 'Peer_VALUE', 'result': 'Mooss', 'unchanged': '보존자료', 'line': 'Zeil', 'server_tcp_port': 'Server_Stream_Port', 'source': '원본자료', 'NetworkBridge': 'Reseau_Bréck', 'jar': '자바꾸러미', 'receive': '수신하기', 'report': 'Validatioun_mellen'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
