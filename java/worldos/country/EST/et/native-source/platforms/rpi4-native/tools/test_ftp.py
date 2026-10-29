#!/usr/bin/env python3
"""기존 RADA 호환 kirje_p. tegelik_andmed 구현: ../Tööriistad/파일전송시험.py"""
import importlib as TAKE_VALUE
import sys as operatsioonisüsteem_VALUE
from pathlib import Path as RADA
operatsioonisüsteem_VALUE.path.insert(0, str(RADA(__file__).resolve().parents[1] / 'Tööriistad'))
if __name__ == '__main__':
    import runpy as programm_käiviti
    programm_käiviti.run_module('파일전송시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('파일전송시험')
    vastendamine_VALUE = {'timeout': '시간제한', 'payload': 'last_andmed', 'broken': '손상자료', 'linux_example': '리눅스예제', 'chunk': '조각', 'data': 'andmed', 'proc': 'Protsess', 'code': '명령열', 'linux': '리눅스파일', 'archive': 'Arhiiv', 'main': 'Käivita_2', 'net_source': 'NET_lähe', 'temporary': '임시자원', 'static_source': '정적원문', 'java_source': '자바원문', 'echo': 'kaja_server_kirje', 'ROOT': 'Project_juur', 'text': 'Tekst', 'marker': 'marker', 'EchoFixture': '되돌림시험서버', 'command': 'Käsk', 'out': 'näitaja_andmed', 'expected': '예상결과', 'server_source': 'server_lähe', 'shell': 'kest', 'upload': 'Upload_Failid', 'transcript': 'transkriptsioon', 'port': 'pordinumber', 'native': '자체실행파일', 'elf': '실행파일', 'server_udp_port': 'server_datagramm_port', 'packed': '묶인자료', 'bridge': 'sild', 'selector': 'valija', 'end': 'lõpeta_kõne_nihe', 'e': '보조항목', 'ftp': 'failiedastus_ühendus', 'key': '누름값', 'bytecode': '바이트코드', 'peer': 'partner_VALUE', 'result': 'TULEMUS', 'unchanged': '보존자료', 'line': 'Joon', 'server_tcp_port': 'server_voog_port', 'source': '원본자료', 'NetworkBridge': 'sild_3de4fe3a', 'jar': '자바꾸러미', 'receive': 'saama_meil', 'report': 'kinnitamine_aruanne'}
    for 이전, tähtaja_piires_kaup in vastendamine_VALUE.items():
        if hasattr(구현, tähtaja_piires_kaup): globals()[이전] = getattr(구현, tähtaja_piires_kaup)
