#!/usr/bin/env python3
"""기존 ụzọ_ozi 호환 ndebà_akara. ǹdịnezie_datà 구현: ../Ngwaọrụ/파일전송시험.py"""
import importlib as 가져오기
import sys as OS_valuu
from pathlib import Path as ụzọ_ozi
OS_valuu.path.insert(0, str(ụzọ_ozi(__file__).resolve().parents[1] / 'Ngwaọrụ'))
if __name__ == '__main__':
    import runpy as app_ihengosi_ndi_app
    app_ihengosi_ndi_app.run_module('파일전송시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('파일전송시험')
    대응 = {'timeout': '시간제한', 'payload': 'ebe_mbulingwa_datà', 'broken': '손상자료', 'linux_example': '리눅스예제', 'chunk': '조각', 'data': 'datà', 'proc': 'ùsòrò', 'code': 'okwunkụzi_NSOTANSO', 'linux': '리눅스파일', 'archive': 'ọkpụ', 'main': 'Bido', 'net_source': '통신원문', 'temporary': '임시자원', 'static_source': 'adịmgbanwò_ebensìbịa', 'java_source': '자바원문', 'echo': '되돌림서버항목', 'ROOT': '기준', 'text': 'SMS', 'marker': '확인표시', 'EchoFixture': '되돌림시험서버', 'command': 'Ntiiwu', 'out': '결과자료', 'expected': '예상결과', 'server_source': 'savà_ebensìbịa', 'shell': 'nkọwannyemiwu', 'upload': 'bùlie_Ndi_ọbọakwụkwọ', 'transcript': '대화기록', 'port': '접속번호', 'native': '자체실행파일', 'elf': '실행파일', 'server_udp_port': '서버전문접속번호', 'packed': '묶인자료', 'bridge': '연결다리', 'selector': 'ihe_nhọpụta', 'end': 'mèdebe_Nnokwata', 'e': '보조항목', 'ftp': 'ọbọakwụkwọ_dògharịa_njikọ', 'key': '누름값', 'bytecode': '바이트코드', 'peer': 'ibè_valuu', 'result': '결과', 'unchanged': '보존자료', 'line': 'ahịrī', 'server_tcp_port': 'savà_agịrị_pọọt', 'source': '원본자료', 'NetworkBridge': '통신다리', 'jar': '자바꾸러미', 'receive': '수신하기', 'report': 'nkwèputaonòdù_akụkọ'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
