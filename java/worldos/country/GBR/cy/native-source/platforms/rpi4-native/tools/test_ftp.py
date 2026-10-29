#!/usr/bin/env python3
"""기존 LLWYBR 호환 cofnod_p. go_iawn_data 구현: ../Offer/파일전송시험.py"""
import importlib as TAKE_VALUE
import sys as system_weithredu_VALUE
from pathlib import Path as LLWYBR
system_weithredu_VALUE.path.insert(0, str(LLWYBR(__file__).resolve().parents[1] / 'Offer'))
if __name__ == '__main__':
    import runpy as Rhaglen_lansiwr
    Rhaglen_lansiwr.run_module('파일전송시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('파일전송시험')
    대응 = {'timeout': '시간제한', 'payload': 'llwyth_uchaf_data', 'broken': '손상자료', 'linux_example': '리눅스예제', 'chunk': '조각', 'data': 'data', 'proc': 'Proses', 'code': 'cyfarwyddyd_SEQUENCE', 'linux': '리눅스파일', 'archive': 'Archif', 'main': 'Gweithredu_2', 'net_source': '통신원문', 'temporary': '임시자원', 'static_source': 'statig_ffynhonnell', 'java_source': '자바원문', 'echo': '되돌림서버항목', 'ROOT': 'prosiect_gwraidd', 'text': 'Testun', 'marker': '확인표시', 'EchoFixture': '되돌림시험서버', 'command': 'Gorchymyn', 'out': 'mesur_data', 'expected': '예상결과', 'server_source': 'gweinydd_ffynhonnell', 'shell': 'cragen', 'upload': 'Upload_Ffeil', 'transcript': '대화기록', 'port': 'rhif_porth', 'native': '자체실행파일', 'elf': '실행파일', 'server_udp_port': '서버전문접속번호', 'packed': '묶인자료', 'bridge': 'pont', 'selector': 'dewisydd', 'end': 'gorffen_OFFSET', 'e': '보조항목', 'ftp': 'ffeil_trosglwyddo_cyswllt', 'key': '누름값', 'bytecode': '바이트코드', 'peer': 'cymar_VALUE', 'result': 'mesur', 'unchanged': '보존자료', 'line': 'llinell', 'server_tcp_port': 'gweinydd_ffrwd_porth', 'source': '원본자료', 'NetworkBridge': 'Rhwydwaith_pont', 'jar': '자바꾸러미', 'receive': '수신하기', 'report': 'dilysu_adrodd'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
