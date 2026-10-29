#!/usr/bin/env python3
"""기존 Ýol 호환 girizmeklik_utuk. hakyky_maglumat 구현: ../Gurallar/파일전송시험.py"""
import importlib as 가져오기
import sys as operasiýa_ulgamy_baha
from pathlib import Path as Ýol
operasiýa_ulgamy_baha.path.insert(0, str(Ýol(__file__).resolve().parents[1] / 'Gurallar'))
if __name__ == '__main__':
    import runpy as programma_programma_paneli
    programma_programma_paneli.run_module('파일전송시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('파일전송시험')
    대응 = {'timeout': '시간제한', 'payload': 'ýük_gutujygy_maglumat', 'broken': '손상자료', 'linux_example': '리눅스예제', 'chunk': '조각', 'data': 'maglumat', 'proc': 'Proses', 'code': 'instruksiýa_SEQUENCE', 'linux': '리눅스파일', 'archive': 'Arhiw', 'main': 'Bitir', 'net_source': '통신원문', 'temporary': '임시자원', 'static_source': 'statiki_gor', 'java_source': '자바원문', 'echo': '되돌림서버항목', 'ROOT': '기준', 'text': 'Metin', 'marker': '확인표시', 'EchoFixture': '되돌림시험서버', 'command': 'buýruk', 'out': '결과자료', 'expected': '예상결과', 'server_source': 'serwer_gor', 'shell': 'gabyjak', 'upload': 'ýükle_Faýllar', 'transcript': '대화기록', 'port': '접속번호', 'native': '자체실행파일', 'elf': '실행파일', 'server_udp_port': '서버전문접속번호', 'packed': '묶인자료', 'bridge': '연결다리', 'selector': 'saýlaýjy', 'end': 'tamamla_Süýşüriş', 'e': '보조항목', 'ftp': 'faýl_geçir_birikme', 'key': '누름값', 'bytecode': '바이트코드', 'peer': 'deň_derejeli_düwün_baha', 'result': '결과', 'unchanged': '보존자료', 'line': 'setir', 'server_tcp_port': 'serwer_Stream_port', 'source': '원본자료', 'NetworkBridge': '통신다리', 'jar': '자바꾸러미', 'receive': '수신하기', 'report': 'barlag_hasabat'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
