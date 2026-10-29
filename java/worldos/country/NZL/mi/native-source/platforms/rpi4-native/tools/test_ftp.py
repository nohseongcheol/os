#!/usr/bin/env python3
"""기존 ara 호환 tāurunga_ira. tūturu_raraunga 구현: ../Ngā_Utauta/파일전송시험.py"""
import importlib as TAKE_uara
import sys as pūnaha_mahi_uara
from pathlib import Path as ara
pūnaha_mahi_uara.path.insert(0, str(ara(__file__).resolve().parents[1] / 'Ngā_Utauta'))
if __name__ == '__main__':
    import runpy as kaupapa_pūwhiri_taupānga
    kaupapa_pūwhiri_taupānga.run_module('파일전송시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_uara.import_module('파일전송시험')
    대응 = {'timeout': '시간제한', 'payload': 'tino_raraunga_raraunga', 'broken': '손상자료', 'linux_example': '리눅스예제', 'chunk': '조각', 'data': 'raraunga', 'proc': 'Hātepe', 'code': 'tohutohu_SEQUENCE', 'linux': '리눅스파일', 'archive': 'Pūranga', 'main': 'whakahaere', 'net_source': '통신원문', 'temporary': '임시자원', 'static_source': 'pateko_pūtake', 'java_source': '자바원문', 'echo': '되돌림서버항목', 'ROOT': 'whakaatu_pūtake', 'text': 'Ngā_kupu', 'marker': '확인표시', 'EchoFixture': '되돌림시험서버', 'command': 'tono', 'out': 'mēhua_raraunga', 'expected': '예상결과', 'server_source': 'tūmau_pūtake', 'shell': 'anga', 'upload': 'tukuatu_Ngā_Kōnae', 'transcript': '대화기록', 'port': '접속번호', 'native': '자체실행파일', 'elf': '실행파일', 'server_udp_port': '서버전문접속번호', 'packed': '묶인자료', 'bridge': 'arawhata', 'selector': 'pūtīpako', 'end': 'mutu_OFFSET', 'e': '보조항목', 'ftp': 'kōnae_whakawhiti_hononga', 'key': '누름값', 'bytecode': '바이트코드', 'peer': 'hoa_uara', 'result': 'mēhua', 'unchanged': '보존자료', 'line': 'hononga', 'server_tcp_port': 'tūmau_roma_kawe', 'source': '원본자료', 'NetworkBridge': 'whatunga_arawhata', 'jar': '자바꾸러미', 'receive': '수신하기', 'report': 'whakamana_pūrongo'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
