#!/usr/bin/env python3
"""기존 yo_l 호환 kiritish_nuqta. real_ma_lumotlar 구현: ../Vositalar/파일전송시험.py"""
import importlib as TAKE_VALUE
import sys as operatsion_tizim_VALUE
from pathlib import Path as yo_l
operatsion_tizim_VALUE.path.insert(0, str(yo_l(__file__).resolve().parents[1] / 'Vositalar'))
if __name__ == '__main__':
    import runpy as ilova_ilovalar_paneli
    ilova_ilovalar_paneli.run_module('파일전송시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('파일전송시험')
    대응 = {'timeout': '시간제한', 'payload': 'foydali_yuklanma_ma_lumotlar', 'broken': '손상자료', 'linux_example': '리눅스예제', 'chunk': '조각', 'data': 'ma_lumotlar', 'proc': 'Jarayon', 'code': 'qo_llanma_SEQUENCE', 'linux': '리눅스파일', 'archive': 'Arxiv', 'main': 'Bajarish', 'net_source': '통신원문', 'temporary': '임시자원', 'static_source': 'statik_manba', 'java_source': '자바원문', 'echo': '되돌림서버항목', 'ROOT': 'Project_ildiz', 'text': 'Matn', 'marker': '확인표시', 'EchoFixture': '되돌림시험서버', 'command': 'Buyruq', 'out': 'o_lchov_ma_lumotlar', 'expected': '예상결과', 'server_source': 'server_manba', 'shell': 'qobiq', 'upload': 'uzatmoq_Fayllar', 'transcript': '대화기록', 'port': '접속번호', 'native': '자체실행파일', 'elf': '실행파일', 'server_udp_port': '서버전문접속번호', 'packed': '묶인자료', 'bridge': '연결다리', 'selector': 'tanlagich', 'end': 'to_xtatmoq_OFFSET', 'e': '보조항목', 'ftp': 'fayl_uzatish_aloqa', 'key': '누름값', 'bytecode': '바이트코드', 'peer': 'bir_rangli_VALUE', 'result': 'o_lchov', 'unchanged': '보존자료', 'line': 'satr', 'server_tcp_port': 'server_oqim_port', 'source': '원본자료', 'NetworkBridge': '통신다리', 'jar': '자바꾸러미', 'receive': '수신하기', 'report': 'tasdiq_hisobot'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
