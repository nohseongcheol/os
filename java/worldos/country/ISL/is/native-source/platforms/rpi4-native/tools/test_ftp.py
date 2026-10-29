#!/usr/bin/env python3
"""기존 SLÓÐ 호환 færsla_P. raun_gögn 구현: ../Verkfæri/파일전송시험.py"""
import importlib as TAKE_VALUE
import sys as stýrikerfi_VALUE
from pathlib import Path as SLÓÐ
stýrikerfi_VALUE.path.insert(0, str(SLÓÐ(__file__).resolve().parents[1] / 'Verkfæri'))
if __name__ == '__main__':
    import runpy as forrit_ræsir
    forrit_ræsir.run_module('파일전송시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('파일전송시험')
    vörpun_VALUE = {'timeout': '시간제한', 'payload': 'farmur_gögn', 'broken': '손상자료', 'linux_example': '리눅스예제', 'chunk': '조각', 'data': 'gögn', 'proc': 'Ferli', 'code': 'skipun_SEQUENCE', 'linux': '리눅스파일', 'archive': 'Safn', 'main': 'Keyra_2', 'net_source': 'nettó_uppruni', 'temporary': '임시자원', 'static_source': 'fast_uppruni', 'java_source': '자바원문', 'echo': '되돌림서버항목', 'ROOT': 'verk_rót', 'text': 'Texti', 'marker': '확인표시', 'EchoFixture': '되돌림시험서버', 'command': 'Skipun', 'out': 'mæld_stærð_gögn', 'expected': '예상결과', 'server_source': 'þjónn_uppruni', 'shell': 'skel', 'upload': 'hlaða_upp_Skrár', 'transcript': '대화기록', 'port': 'tengisnúmer', 'native': '자체실행파일', 'elf': '실행파일', 'server_udp_port': '서버전문접속번호', 'packed': '묶인자료', 'bridge': 'brú', 'selector': 'val', 'end': 'ljúka_OFFSET', 'e': '보조항목', 'ftp': 'skrá_flytja_tenging', 'key': '누름값', 'bytecode': '바이트코드', 'peer': 'jafningi_VALUE', 'result': 'NIÐURSTAÐA', 'unchanged': '보존자료', 'line': 'Lína', 'server_tcp_port': 'þjónn_Stream_gátt', 'source': '원본자료', 'NetworkBridge': 'Net_brú', 'jar': '자바꾸러미', 'receive': '수신하기', 'report': 'prófun_skrá'}
    for 이전, 현재 in vörpun_VALUE.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
