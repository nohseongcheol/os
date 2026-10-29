#!/usr/bin/env python3
"""기존 Pad 호환 inskrywing_p. werklik_data 구현: ../Nutsmiddels/파일전송시험.py"""
import importlib as TAKE_VALUE
import sys as bedryfstelsel_VALUE
from pathlib import Path as Pad
bedryfstelsel_VALUE.path.insert(0, str(Pad(__file__).resolve().parents[1] / 'Nutsmiddels'))
if __name__ == '__main__':
    import runpy as program_oopmaker
    program_oopmaker.run_module('파일전송시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('파일전송시험')
    대응 = {'timeout': '시간제한', 'payload': 'lading_data', 'broken': '손상자료', 'linux_example': '리눅스예제', 'chunk': '조각', 'data': 'data', 'proc': 'Proses', 'code': 'instruksie_SEQUENCE', 'linux': '리눅스파일', 'archive': 'Argief', 'main': 'Loop', 'net_source': '통신원문', 'temporary': '임시자원', 'static_source': 'staties_bron', 'java_source': '자바원문', 'echo': '되돌림서버항목', 'ROOT': 'Project_wortel', 'text': 'Teks', 'marker': '확인표시', 'EchoFixture': '되돌림시험서버', 'command': 'Opdrag', 'out': 'maatreël_data', 'expected': '예상결과', 'server_source': 'bediener_bron', 'shell': 'dop', 'upload': 'oplaai_Lêers', 'transcript': '대화기록', 'port': '접속번호', 'native': '자체실행파일', 'elf': '실행파일', 'server_udp_port': '서버전문접속번호', 'packed': '묶인자료', 'bridge': 'brug', 'selector': 'selekteerder', 'end': 'beëindig_OFFSET', 'e': '보조항목', 'ftp': 'lêer_oordra_verbinding', 'key': '누름값', 'bytecode': '바이트코드', 'peer': 'portuur_VALUE', 'result': 'maatreël', 'unchanged': '보존자료', 'line': 'lyn', 'server_tcp_port': 'bediener_Stream_ombou', 'source': '원본자료', 'NetworkBridge': 'Netwerk_brug', 'jar': '자바꾸러미', 'receive': '수신하기', 'report': 'validering_verslag'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
