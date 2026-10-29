#!/usr/bin/env python3
"""기존 POZICIONI 호환 futje_p. aktual_të_dhëna 구현: ../Mjete/파일전송시험.py"""
import importlib as TAKE_VALUE
import sys as sistem_operativ_VALUE
from pathlib import Path as POZICIONI
sistem_operativ_VALUE.path.insert(0, str(POZICIONI(__file__).resolve().parents[1] / 'Mjete'))
if __name__ == '__main__':
    import runpy as program_hapës
    program_hapës.run_module('파일전송시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('파일전송시험')
    대응 = {'timeout': '시간제한', 'payload': 'ngarkesë_e_dobishme_të_dhëna', 'broken': '손상자료', 'linux_example': '리눅스예제', 'chunk': '조각', 'data': 'të_dhëna', 'proc': 'Proçes', 'code': 'instruksion_SEQUENCE', 'linux': '리눅스파일', 'archive': 'arkiv', 'main': 'Ekzekuto', 'net_source': '통신원문', 'temporary': '임시자원', 'static_source': 'statik_burim', 'java_source': '자바원문', 'echo': '되돌림서버항목', 'ROOT': 'Project_rrënjë', 'text': 'Teksti', 'marker': '확인표시', 'EchoFixture': '되돌림시험서버', 'command': 'Komanda', 'out': 'llogaritje_të_dhëna', 'expected': '예상결과', 'server_source': 'server_burim', 'shell': 'pasues', 'upload': 'Ngarkim_Skedarët', 'transcript': '대화기록', 'port': 'numri_i_portës', 'native': '자체실행파일', 'elf': '실행파일', 'server_udp_port': '서버전문접속번호', 'packed': '묶인자료', 'bridge': 'urë', 'selector': 'përzgjedhësi', 'end': 'mbaroj_OFFSET', 'e': '보조항목', 'ftp': 'skedar_transferim_lidhje', 'key': '누름값', 'bytecode': '바이트코드', 'peer': 'homolog_VALUE', 'result': 'llogaritje', 'unchanged': '보존자료', 'line': 'linjë', 'server_tcp_port': 'server_Stream_portë', 'source': '원본자료', 'NetworkBridge': 'rrjet_urë', 'jar': '자바꾸러미', 'receive': '수신하기', 'report': 'miratim_raport'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
